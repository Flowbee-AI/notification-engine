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
exports.oneSignalClient = void 0;
require("dotenv").config();
class OneSignalClient {
    constructor() {
        this.url = "https://api.onesignal.com/notifications?c=push";
        this.apiKey = process.env.ONESIGNAL_API_KEY;
        this.appId = process.env.ONESIGNAL_APP_ID;
        if (!this.apiKey || !this.appId) {
            throw new Error("OneSignal API Key or App ID is not provided");
        }
    }
    static getInstance() {
        if (!this.instance) {
            this.instance = new OneSignalClient();
        }
        return this.instance;
    }
    sendNotification(data) {
        return __awaiter(this, void 0, void 0, function* () {
            if (data.payload.type == "BUILDER") {
                console.log("Sending notification to builder");
                return yield this.sendNotificationBuilder(data);
            }
            else {
                return yield this.sendNotificationIdeation(data);
            }
        });
    }
    sendNotificationBuilder(data) {
        return __awaiter(this, void 0, void 0, function* () {
            let { title, description, imageUrl, type, link } = data.payload;
            let userId = data.userId;
            let res = yield fetch(this.url, {
                method: "POST",
                headers: {
                    "accept": 'application/json',
                    "Content-Type": "application/json",
                    "Authorization": `Key ${this.apiKey}`
                },
                body: JSON.stringify({
                    "app_id": this.appId,
                    "contents": { "en": description },
                    "headings": { "en": title },
                    "big_picture": imageUrl,
                    "include_aliases": {
                        "external_id": [
                            userId
                        ]
                    },
                    "target_channel": "push"
                })
            });
            let onesignalData = yield res.json();
            console.log(onesignalData);
            return onesignalData;
        });
    }
    sendNotificationIdeation(data) {
        return __awaiter(this, void 0, void 0, function* () {
            let { title, description, imageUrl, type, link } = data.payload;
            let userId = data.userId;
            let res = yield fetch(this.url, {
                method: "POST",
                headers: {
                    "accept": 'application/json',
                    "Content-Type": "application/json",
                    "Authorization": `Key ${this.apiKey}`
                },
                body: JSON.stringify({
                    "app_id": this.appId,
                    "contents": { "en": description },
                    "headings": { "en": title },
                    "big_picture": imageUrl,
                    "include_external_user_ids": [
                        userId
                    ],
                    "delayed_option": "timezone",
                    "delivery_time_of_day": "9:00AM"
                })
            });
            let onesignalData = yield res.json();
            return onesignalData;
        });
    }
}
exports.oneSignalClient = OneSignalClient.getInstance();
