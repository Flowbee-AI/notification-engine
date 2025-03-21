require("dotenv").config();
import { QueueJobType } from "../modules/queue/queue.model";


export type OneSignalResponsetype = {
    id: string;
    errors: string[]
}

class OneSignalClient {
    private url: string = "https://api.onesignal.com/notifications?c=push";
    private apiKey: string | undefined = process.env.ONESIGNAL_API_KEY;
    private appId: string | undefined = process.env.ONESIGNAL_APP_ID;
    public static instance: OneSignalClient;
    private constructor() {
        if (!this.apiKey || !this.appId) {
            throw new Error("OneSignal API Key or App ID is not provided");
        }
    }
    public static getInstance() {
        if (!this.instance) {
            this.instance = new OneSignalClient();
        }
        return this.instance;
    }

    public async sendNotification(data: QueueJobType): Promise<OneSignalResponsetype> {
        if (data.payload.type == "BUILDER") {
            console.log("Sending notification to builder")
            return await this.sendNotificationBuilder(data);
        }
        else {

            return await this.sendNotificationIdeation(data);
        }
    }
    public async sendNotificationBuilder(data: QueueJobType) {
        let { title, description, imageUrl, type, link } = data.payload;
        let userId = data.userId;
        let res = await fetch(this.url, {
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
        })
        
        let onesignalData: any = await res.json();
        console.log(onesignalData)
        return onesignalData;

    }
    public async sendNotificationIdeation(data: QueueJobType) {
        let { title, description, imageUrl, type, link } = data.payload;
        let userId = data.userId;
        let res = await fetch(this.url, {
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
        })
        let onesignalData: OneSignalResponsetype = await res.json();
        return onesignalData
    }
}
export const oneSignalClient = OneSignalClient.getInstance()