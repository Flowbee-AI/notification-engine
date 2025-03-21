export type QueueJobType = {
    userId: string;
    payload: {
        type : "IDEATION"  | "BUILDER"
        title : string 
        description: string
        imageUrl ?: string;
        link ?: string;
    }; 
    
}