from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import dirname
import os
from argparse import ArgumentParser
from pdb import set_trace
from sys import stderr

try:
    from ncr_web import __file__ as ncr_web_file
    files_root = dirname(ncr_web_file) + '/build/'
except ImportError:
    file_dir = dirname(__file__)
    if len(file_dir) > 0:
        file_dir += '/'
    files_root =file_dir + '../web/build/'

# Tutorial: https://pythonbasics.org/webserver/

hostName = 'localhost'

def parse_args():
    parser = ArgumentParser(prog='ncrserver',
        description='Creates local ncreview data server.')
    parser.add_argument('-p', '--port', 
        help="Port for the ncrserver to listen to.",
        type=int, default=8000)
    return parser.parse_args()

def ends_with(haystack, needle):
    length = len(needle)
    if not length:
        return True
    return haystack[-length:] == needle

class NCRPageServer(BaseHTTPRequestHandler):
    ncr_data_paths = ['/data/tmp', '/data/tmp-engr']

    def __init__(self, request, client_address, server):
        self.files_root = files_root
        self.path_endpoint = '/ncreview/'
        super().__init__(request, client_address, server)

    def get_file_location(self) -> str:
        # Assumption: do_GET already verified we're at the /ncreview/ endpoint
        file_location = self.path[len(self.path_endpoint):]
        args_index = file_location.find('?')
        if args_index != -1:
            file_location = file_location[:args_index]
        print(file_location)
        # if the entire path was /ncreview/?args
        if len(file_location) == 0:
            return self.files_root + 'index.html'
        return self.files_root + file_location

    def do_GET(self):
        #self.tutorial_response()
        #return

        if self.path_endpoint not in self.path:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

        return_file = self.get_file_location()
        try:
            if os.path.basename(return_file) == 'data.php':
                self.handle_data_php_request()
                return

            with open(return_file, 'rb') as infile:
                response_bytes = infile.read()

            #file_ext = return_file[return_file.rfind('.'):]
            #if file_ext == '.php':
            #    content_type = 'application/json'
            #else:
             #   content_type = 'text/html'
            content_type = 'text/html'

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response_bytes)

        except FileNotFoundError:
            self.send_response(404, "file not found")
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def tutorial_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def get_args(self) -> dict:
        args_index = self.path.rfind('?')
        if args_index == -1:
            return {}
        args_str = self.path[args_index + 1:]
        keyvalue_strs = args_str.split('&')
        keyvalue_tuples = [string.split('=') for string in keyvalue_strs]
        return { pair[0] : pair[1] for pair in keyvalue_tuples }

    def handle_data_php_request(self):
        try:
            return_data = self.get_ncreview_data()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(return_data)

        except ValueError:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        except Exception as e:
            self.send_response(500, f'Server error: {str(e)}')
            self.send_header("Content-type", "text/html")
            self.end_headers()

    # Ported from the data.php file
    # so it can be called on systems without the PHP executable
    # Throws:
    # ValueError: if needed parameters are not present
    # FileNotFoundError: if no directory matching id, or no file matching id and num
    def get_ncreview_data(self) -> bytes:
        args = self.get_args()
        if 'id' not in args:
            raise ValueError("Request must specify an id")

        # TODO: id and num really need to be validated.
        #   - num should definitely be only a set of digits.
        #   - How to validate id as an arbitrary directory?
        #   - We do *always* append final filenames to path (.json or .csv) (so validating num is critical),
        #       but that doesn't mean id can't be something arbitrarily detrimental.
        
        path = ""

        id = args['id']
        if '/' in id:
            path = id
            if not ends_with(path, '/'):
                path += '/'
        else:
            dirs = self.ncr_data_paths
            for dir in dirs:
                p = f"{dir}/ncreview/{id}/"
                if os.path.exists(p) and os.access(p, os.R_OK):
                    path = p
                    break
            if not path:
                error_message = f"Cannot find directory ncreview/{id} in any of ("
                for dir in dirs:
                    error_message += f'{dir}, '
                error_message += ')'
                raise FileNotFoundError(error_message)

        if 'num' not in args:
            path += "ncreview.json"
        else:
            try:
                dummy = int(args['num'])
            except ValueError:
                raise ValueError(f'Expected integer for "num" arg (got {args["num"]})')

            path += f"ncreview.{args['num']}.csv"

        if not os.path.exists(path) or not os.access(path, os.R_OK):
            raise FileNotFoundError(f"File {path} is unreadable or does not exist.")

        with open(path, 'rb') as file:
            return file.read()

def main():
    args = parse_args()

    try:
        webServer = HTTPServer((hostName, args.port), NCRPageServer)
    except OSError as e:
        if e.errno == 98: # address already in use
            print(f'Port {args.port} already in use. ' + 
                'Please open the SSH tunnel to a new port and try again.')
            exit(1)
        else:
            raise e

    print("Server started http://%s:%s" % (hostName, args.port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":        
    main()
