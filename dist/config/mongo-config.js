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
Object.defineProperty(exports, "__esModule", { value: true });
exports.MongoConfig = void 0;
require("dotenv").config();
const mongodb_1 = require("mongodb");
class MongoConfig {
    constructor() {
        this.url = process.env.MONGO_URL;
        this.dbName = process.env.MONGO_DB_NAME;
        if (this.url == null || this.url == "" || this.url == undefined || this.url.length == 0) {
            throw new Error("Mongo URL not found");
        }
        if (this.dbName == null || this.dbName == "" || this.dbName == undefined || this.dbName.length == 0) {
            throw new Error("Mongo DB Name not found");
        }
        this.client = new mongodb_1.MongoClient(this.url);
        if (!this.client) {
            throw new Error("Mongo Client not initialized");
        }
        this.db = this.client.db(this.dbName);
        if (!this.db) {
            throw new Error("Mongo DB not initialized");
        }
    }
    static getInstance() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!this.instance) {
                this.instance = new MongoConfig();
                if (!this.instance.client) {
                    throw new Error("MongoClient is not initialized");
                }
                yield this.instance.client.connect();
                console.log("mongo client connected successfully");
            }
            return MongoConfig.instance;
        });
    }
    getClient() {
        return this.client;
    }
}
exports.MongoConfig = MongoConfig;
