"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const dotenv_1 = __importDefault(require("dotenv"));
const http_1 = require("http");
const socket_io_1 = require("socket.io");
const fs_1 = __importDefault(require("fs"));
const readline_1 = __importDefault(require("readline"));
let readStream = null;
console.log(process.env.NODE_ENV);
if (process.env.NODE_ENV === 'production') {
    readStream = fs_1.default.createReadStream('dagensalbum.log');
}
else {
    readStream = fs_1.default.createReadStream('../logs/dagensalbum.log');
}
const logs = [];
const rl = readline_1.default.createInterface({
    input: readStream,
    crlfDelay: Infinity
});
rl.on('line', (line) => {
    logs.push(line);
});
rl.on('close', () => {
    console.log('Finished reading file.');
});
const Tail = require('tail').Tail;
let tail = null;
if (process.env.NODE_ENV === 'production') {
    tail = new Tail('dagensalbum.log');
}
else {
    tail = new Tail('../logs/dagensalbum.log');
}
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT ? process.env.PORT : 3000;
const httpServer = (0, http_1.createServer)(app);
httpServer.listen(port, () => {
    console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
const io = new socket_io_1.Server(httpServer);
app.set('view engine', 'pug');
tail.on('line', (data) => {
    logs.push(data);
    console.log(typeof (data));
    io.emit('log', data);
});
app.get('/socket.io/socket.io.js', (req, res) => {
    res.sendFile(__dirname + '/node_modules/socket.io-client/dist/socket.io.js');
});
app.get('/', (req, res) => {
    res.send('Express + TypeScript Server');
});
app.get('/logs', (req, res) => {
    const logFile = fs_1.default.readFileSync('../logs/dagensalbum.log', 'utf-8');
    console.log(logFile);
    res.render('../renderings/index', { logs: logs });
});
io.on('connection', (socket) => {
    console.log('a user connected');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});
