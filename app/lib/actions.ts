'use server';

import { sql } from '@vercel/postgres';
import {auth, signIn} from '@/auth';
import { AuthError } from 'next-auth';


export async function fetchProducts(customer: any): Promise<{ teil_name: string }[]> {
  // throw new Error('Failed to Delete Invoice');
  const session = await auth();
  try {
    const products = await sql`
    SELECT DISTINCT teil_name
    FROM (
        SELECT teil_name
        FROM sales
        WHERE user_id = ${session?.user?.email} AND kunde_name = ${customer}
        GROUP BY teil_name
        HAVING COUNT(DISTINCT woche) >= 20
    ) AS subquery`;

    return products.rows.map(row => ({ teil_name: row.teil_name }));
  } catch (error) {
    console.log('Database Error: Failed to Fetch Products for Customer.' );
    return [];
  }
}


export async function fetchSales(customer: any, product:any): Promise<{ 'Verkaufte Menge': number, datum: Date }[]> {
  // throw new Error('Failed to Delete Invoice');
  const session = await auth();
  try {
    const sales = await sql`
        SELECT menge, woche 
        FROM sales 
        WHERE kunde_name = ${customer} AND teil_name = ${product} AND user_id = ${session?.user?.email}
        ORDER BY woche;
        `;
    return sales.rows.map(row => ({ 'Verkaufte Menge': row.menge, datum: row.woche }));
  } catch (error) {
    console.log('Database Error: Failed to Fetch Products for Customer.' );
    return [];
  }
}


export async function authenticate(
  prevState: string | undefined,
  formData: FormData,
) {
  try {
    await signIn('credentials', formData);
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case 'CredentialsSignin':
          return 'Invalid credentials.';
        default:
          return 'Something went wrong.';
      }
    }
    throw error;
  }
}
