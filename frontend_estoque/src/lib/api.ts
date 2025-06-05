import { IProductStock } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getStock(): Promise<IProductStock[]> {
    try {
        const response = await fetch(`${API_URL}/estoque`, {
            //Garantir os dados mais recentes
            cache: 'no-cache',
        });
        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }
        const responseData = await response.json();
        return responseData.data || [];
    } catch (error) {
        console.error("Failed to fetch stock data:", error);
        throw error; // Re-throw the error for further handling
    }
}