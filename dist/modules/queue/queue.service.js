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
exports.queueService = void 0;
require("dotenv").config();
const rabbitmq_1 = __importDefault(require("./rabbitmq"));
class Queue {
    constructor() {
        this.initialized = false;
        this.queueName = process.env.RABBITMQ_NAME;
        if (this.queueName == null || this.queueName == "" || this.queueName == undefined || this.queueName.length == 0) {
            throw new Error("Queue name not found");
        }
        console.log("Queue created");
    }
    static getInstance() {
        if (!Queue.instance) {
            Queue.instance = new Queue();
        }
        return Queue.instance;
    }
    setupQueue() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.initialized)
                return;
            const rabbitMQ = yield rabbitmq_1.default.getInstance();
            const channel = rabbitMQ.getChannel();
            yield channel.assertQueue(this.queueName, { durable: true });
            this.initialized = true;
            console.log(`🚀 Queue Initialized: ${this.queueName}`);
        });
    }
}
exports.queueService = Queue.getInstance();
