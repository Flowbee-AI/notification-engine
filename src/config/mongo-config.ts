require("dotenv").config();
import { Db, MongoClient } from "mongodb";
export class MongoConfig {
    
    public client : MongoClient | undefined;
    private static instance : MongoConfig;
    public db: Db | undefined;
    private url : string | undefined;
    private dbName : string | undefined;
    
    private  constructor() {
        this.url = process.env.MONGO_URL;
        this.dbName = process.env.MONGO_DB_NAME;
        if(this.url==null  || this.url == "" || this.url == undefined || this.url.length == 0){
            throw new Error("Mongo URL not found")
        }
        if(this.dbName==null  || this.dbName == "" || this.dbName == undefined || this.dbName.length == 0){
            throw new Error("Mongo DB Name not found")
        }
        this.client = new MongoClient(this.url);
        if(!this.client){
            throw new Error("Mongo Client not initialized")
        }
        this.db  = this.client.db(this.dbName);
        if(!this.db){
            throw new Error("Mongo DB not initialized")
        }
        
        
    }
    public static async getInstance() {
        if (!this.instance) {
            this.instance= new MongoConfig();
            if (!this.instance.client) {
                throw new Error("MongoClient is not initialized");
            }
            await this.instance.client.connect();
            console.log("mongo client connected successfully")
        }
        
        return MongoConfig.instance;
    }
    public getClient(){
        return this.client;
    }
}   
