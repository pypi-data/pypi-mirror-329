import uvicorn
import imaging_server_kit as serverkit

server = serverkit.Server(algorithm_name="foo", parameters_model=serverkit.Parameters)
app = server.app

if __name__=='__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000)