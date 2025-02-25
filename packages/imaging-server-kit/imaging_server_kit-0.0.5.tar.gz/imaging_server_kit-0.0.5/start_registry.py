import uvicorn
import imaging_server_kit as serverkit

server = serverkit.Registry()
app = server.app

if __name__=='__main__':
    uvicorn.run("start_registry:app", host="0.0.0.0", port=8000)