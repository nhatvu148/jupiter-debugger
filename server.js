const http = require("http");
const websocket = require("ws");
const fs = require("fs");
const Papa = require("papaparse");

const readData = (path, row) => {
  return new Promise(async (resolve, reject) => {
    if (fs.existsSync(path)) {
      const files = await fs.readFileSync(path, "utf8");
      Papa.parse(files, {
        complete: function (results) {
          resolve(results.data[row]);
        },
      });
    } else {
      reject({ error: "Error" });
    }
  });
};

const server = http.createServer((req, res) => {
  res.end("I am connected!");
});

const wss = new websocket.Server({ server });
wss.on("headers", (headers, req) => {
  console.log(headers);
});

wss.on("connection", (ws, req) => {
  let message;
  ws.on("message", async (msg) => {
    message = JSON.parse(msg);

    console.log(message);
    const data = await readData(`${__dirname}/data.txt`, message.row);
    console.log(data);
    ws.send(JSON.stringify(data));
  });
});

server.listen(8088);
