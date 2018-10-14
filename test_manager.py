import sys
from multiprocessing import managers

class Writer:
    def write_tofile(self, data):
        fp = open('test2.txt', 'w')
        fp.write(data)
        fp.close()

    def print(self, data):
        print(data)

    # this will not work, fp cannot be serialized
    def write_fp(self, fp):
        with open("test3.txt", "w") as f:
            f.write(fp.read())

if __name__ == '__main__':
# client code
    if len(sys.argv) >= 2 and sys.argv[1] == "client":
        mg = managers.BaseManager(address=("localhost", 50001), authkey=b'secret')
        mg.register("get_rpc")
        mg.connect()
        writer = mg.get_rpc()
        writer.print("hello")
        writer.write_tofile("this will be save to file in the server")
        with open("test2.txt", "r") as f:
            writer.write_fp(f)

# server code
    mg = managers.BaseManager(address=("", 50001), authkey=b'secret')
    mg.register("get_rpc", lambda: Writer())
    mg.get_server().serve_forever()


