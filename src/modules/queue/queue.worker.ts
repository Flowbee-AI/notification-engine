require("dotenv").config()
import { QueueJobType } from "./queue.model";
import RabbitMQ from "./rabbitmq";


const QUEUE_NAME = process.env.RABBITMQ_NAME!;


class Worker {
  private static instance: Worker;

  private constructor() {
    if(!QUEUE_NAME || QUEUE_NAME.length == 0){
        throw new Error("RABBITMQ_NAME is required");
    }
  } // Prevent multiple instances

  static async getInstance(): Promise<Worker> {
    if (!Worker.instance) {
      Worker.instance = new Worker();
    }
    return Worker.instance;
  }

  public async start(fn: (data: QueueJobType) => Promise<void>) {
    const rabbitMQ = await RabbitMQ.getInstance();
    const channel = rabbitMQ.getChannel();

    channel.consume(
      QUEUE_NAME,
      async (msg) => {
        if (msg) {
          const data : QueueJobType= JSON.parse(msg.content.toString());
          console.log(`✅ Processing job for userId: ${data.userId}`);

          try {
            await fn(data);
            channel.ack(msg); // Acknowledge success
          } catch (error) {
            console.error(`❌ Error processing job: ${error}`);
            channel.nack(msg); // Retry failed jobs
          }
        }
      },
      { noAck: false }
    );

    console.log("🔄 Worker started...");
  }
  public async stop() {
    const rabbitMQ = await RabbitMQ.getInstance();
    await rabbitMQ.getChannel().close();
  }
}

export default Worker;