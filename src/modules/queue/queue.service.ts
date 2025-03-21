require("dotenv").config();
import RabbitMQ from "./rabbitmq";



class Queue {
  private static instance: Queue;
  private initialized = false;
  private queueName : string | undefined 
  private constructor() {
    this.queueName = process.env.RABBITMQ_NAME;
    if(this.queueName==null  || this.queueName == "" || this.queueName == undefined || this.queueName.length == 0){
      throw new Error("Queue name not found")
    }
    console.log("Queue created");
  } 

  public static  getInstance(): Queue {
    if (!Queue.instance) {
      Queue.instance = new Queue();
      
    }
    return Queue.instance;
  }

  public async setupQueue() {
    if (this.initialized) return;
    const rabbitMQ = await RabbitMQ.getInstance();
    const channel = rabbitMQ.getChannel();
    await channel.assertQueue(this.queueName!, { durable: true });
    this.initialized = true;
    console.log(`🚀 Queue Initialized: ${this.queueName}`);
  }
}


export const queueService = Queue.getInstance();