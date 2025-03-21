import amqplib, { Connection, Channel, ChannelModel } from "amqplib";

const RABBITMQ_URL = process.env.RABBITMQ_URL || "amqp://localhost";

class RabbitMQ {
  private static instance: RabbitMQ;
  private connection!: ChannelModel ;
  private channel!: Channel;

  private constructor() {
    
  } // Private constructor to prevent multiple instances

  static async getInstance(): Promise<RabbitMQ> {
    if (!RabbitMQ.instance) {
      RabbitMQ.instance = new RabbitMQ();
      await RabbitMQ.instance.init();
    }
    return RabbitMQ.instance;
  }

  private async init() {
    if(this.connection && this.channel) {
      console.log("🚀 RabbitMQ already initialized")
      return;
    };
    this.connection = await amqplib.connect(RABBITMQ_URL) ;
    this.channel = await this.connection.createChannel();
    console.log("✅ RabbitMQ Connected");
  }

  getChannel(): Channel {
    return this.channel;
  }
}

export default RabbitMQ;