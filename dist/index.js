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
const onesignal_config_1 = require("./config/onesignal-config");
const queue_service_1 = require("./modules/queue/queue.service");
const queue_worker_1 = __importDefault(require("./modules/queue/queue.worker"));
const rabbitmq_1 = __importDefault(require("./modules/queue/rabbitmq"));
function jobFunction(data) {
    return __awaiter(this, void 0, void 0, function* () {
        yield onesignal_config_1.oneSignalClient.sendNotification(data);
    });
}
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        yield queue_service_1.queueService.setupQueue();
        let rabbitMQ = yield rabbitmq_1.default.getInstance();
        let channel = rabbitMQ.getChannel();
        let data = {
            userId: "7DImtD5bCWMiIYdlin5rTOBXLhz1",
            payload: {
                title: "ajeem bhai kya hal chal",
                description: "kaisa lagi ye photo",
                imageUrl: "https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                type: "BUILDER",
                link: "https://www.google.com"
            }
        };
        channel.sendToQueue("notification", Buffer.from(JSON.stringify(data)));
        (yield queue_worker_1.default.getInstance()).start(jobFunction);
    });
}
main();
