import express, { Express, Request, Response } from 'express';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server } from 'socket.io';
import fs from 'fs';
import readline from 'readline';

let readStream = null;
console.log(process.env.NODE_ENV);
if (process.env.NODE_ENV === 'production') {
  readStream = fs.createReadStream('dagensalbum.log');
}
else {
  readStream = fs.createReadStream('../logs/dagensalbum.log');
}
    

const logs: string[] = [];
const rl = readline.createInterface({
  input: readStream,
  crlfDelay: Infinity
});
rl.on('line', (line:any) => {
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
  tail = new Tail('../logs/dagensalbum.log')
}






dotenv.config();

const app: Express = express();
const port = process.env.PORT ? process.env.PORT : 3000;
const httpServer = createServer(app);
httpServer.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});

const io = new Server(httpServer);

app.set('view engine', 'pug');


tail.on('line', (data: any) => {
  logs.push(data);
  console.log(typeof(data));
  io.emit('log', data);
});

app.get('/socket.io/socket.io.js', (req, res) => {
  res.sendFile(__dirname + '/node_modules/socket.io-client/dist/socket.io.js');
});

app.get('/', (req: Request, res: Response) => {
  res.send('Express + TypeScript Server');
});

app.get('/logs', (req: Request, res: Response) => {
  const logFile = fs.readFileSync('../logs/dagensalbum.log', 'utf-8');
  console.log(logFile);
  res.render('../renderings/index', { logs: logs });
});



io.on('connection', (socket: any) => {
  console.log('a user connected');
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

