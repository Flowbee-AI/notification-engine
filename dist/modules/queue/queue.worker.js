"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("dotenv").config();
const rabbitmq_1 = __importDefault(require("./rabbitmq"));
const QUEUE_NAME = process.env.RABBITMQ_NAME;
class Worker {
    constructor() {
        if (!QUEUE_NAME || QUEUE_NAME.length == 0) {
            throw new Error("RABBITMQ_NAME is required");
        }
    } // Prevent multiple instances
    static getInstance() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!Worker.instance) {
                Worker.instance = new Worker();
            }
            return Worker.instance;
        });
    }
    start(fn) {
        return __awaiter(this, void 0, void 0, function* () {
            const rabbitMQ = yield rabbitmq_1.default.getInstance();
            const channel = rabbitMQ.getChannel();
            channel.consume(QUEUE_NAME, (msg) => __awaiter(this, void 0, void 0, function* () {
                if (msg) {
                    const data = JSON.parse(msg.content.toString());
                    console.log(`✅ Processing job for userId: ${data.userId}`);
                    try {
                        yield fn(data);
                        channel.ack(msg); // Acknowledge success
                    }
                    catch (error) {
                        console.error(`❌ Error processing job: ${error}`);
                        channel.nack(msg); // Retry failed jobs
                    }
                }
            }), { noAck: false });
            console.log("🔄 Worker started...");
        });
    }
    stop() {
        return __awaiter(this, void 0, void 0, function* () {
            const rabbitMQ = yield rabbitmq_1.default.getInstance();
            yield rabbitMQ.getChannel().close();
        });
    }
}
exports.default = Worker;
