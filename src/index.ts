import { oneSignalClient } from "./config/onesignal-config";
import { QueueJobType } from "./modules/queue/queue.model";
import { queueService } from "./modules/queue/queue.service"
import Worker from "./modules/queue/queue.worker"
import RabbitMQ from "./modules/queue/rabbitmq";

async function jobFunction(data: QueueJobType){

    await oneSignalClient.sendNotification(data );
}

async function main(){

    await queueService.setupQueue();
    let rabbitMQ = await RabbitMQ.getInstance();
    let channel = rabbitMQ.getChannel();
    let data: QueueJobType = {
        userId: "new_user",
        payload: {
            title: "title ",
            description: "description",
            imageUrl: "https://plus.unsplash.com/premium_photo-1664474619075-644dd191935f?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
            type: "BUILDER",
            link: "https://www.google.com"
        }
    };
    channel.sendToQueue("notification", Buffer.from(JSON.stringify(data)));
    

    (await Worker.getInstance()).start(jobFunction)
    
}

main()