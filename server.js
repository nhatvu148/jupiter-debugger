const http = require("http");
const websocket = require("ws");

const server = http.createServer((req, res) => {
  res.end("I am connected!");
});

const wss = new websocket.Server({ server });
wss.on("headers", (headers, req) => {
  console.log(headers);
});

wss.on("connection", (ws, req) => {
  setTimeout(() => {
    ws.send("Welcome to the websocket server!! after 3000 ms");
  }, 3000);
  ws.on("message", (msg) => {
    console.log(msg);
  });
});

server.listen(8088);
