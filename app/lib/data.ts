import { sql } from '@vercel/postgres';
import {
  User,
} from './definitions';
import { unstable_noStore as noStore } from 'next/cache';
import { auth } from '@/auth';


export async function fetchCustomers() {
  noStore();
  const session = await auth();
  try {
    const customers = await sql`
    SELECT DISTINCT kunde_name
    FROM (
        SELECT kunde_name
        FROM sales
        WHERE user_id = ${session?.user?.email}
        GROUP BY kunde_name, teil_name
        HAVING COUNT(DISTINCT woche) >= 20
    ) AS subquery`;

    return customers.rows;
  } catch (error) {
    console.error('Database Error:', error);
    throw new Error('Failed to fetch customers.');
  }
}

export async function getUser(email: string) {
  try {
    const user = await sql`SELECT * FROM users WHERE email=${email}`;
    return user.rows[0] as User;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw new Error('Failed to fetch user.');
  }
}
