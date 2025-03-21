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
const amqplib_1 = __importDefault(require("amqplib"));
const RABBITMQ_URL = process.env.RABBITMQ_URL || "amqp://localhost";
class RabbitMQ {
    constructor() {
    } // Private constructor to prevent multiple instances
    static getInstance() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!RabbitMQ.instance) {
                RabbitMQ.instance = new RabbitMQ();
                yield RabbitMQ.instance.init();
            }
            return RabbitMQ.instance;
        });
    }
    init() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.connection && this.channel) {
                console.log("🚀 RabbitMQ already initialized");
                return;
            }
            ;
            this.connection = yield amqplib_1.default.connect(RABBITMQ_URL);
            this.channel = yield this.connection.createChannel();
            console.log("✅ RabbitMQ Connected");
        });
    }
    getChannel() {
        return this.channel;
    }
}
exports.default = RabbitMQ;
