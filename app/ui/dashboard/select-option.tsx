'use client';

import {SearchSelect, SearchSelectItem} from "@tremor/react";
import {useState, useEffect} from "react";
import { auth } from "@/auth"
import {fetchProducts, fetchSales} from "@/app/lib/actions";
import {QueryResultRow} from "pg";
import { LineChart } from '@tremor/react';



export default function SelectOption(customers: any) {
    const [customer, setCustomer] = useState('');
    const [product, setProduct] = useState('');
    const [products, setProducts] = useState<{ teil_name: string }[]>([]);
    const [sales, setSales] = useState<{ 'Verkaufte Menge': number, datum: Date }[]>([]);


    useEffect(() => {
        if(customer) {
            fetchProducts(customer).then((fetchedProducts) => {
                setProducts(fetchedProducts);
            });
        }
    }, [customer]);

    useEffect(() => {
        if (product && customer) {
            fetchSales(customer, product).then((fetchedSales) => {
                setSales(fetchedSales);
            });
        }
    }, [product]);

    return (
        <>
            <div>
                <SearchSelect value={customer} onValueChange={setCustomer}>
                    {customers.customers.map((customer: any) => (
                        <SearchSelectItem key={customer.kunde_name} value={customer.kunde_name}>
                            {customer.kunde_name}
                        </SearchSelectItem>
                    ))}
                </SearchSelect>
            </div>
            <div>
                <SearchSelect value={product} onValueChange={setProduct}>
                    {products.map((product: any) => (
                        <SearchSelectItem key={product.teil_name} value={product.teil_name}>
                            {product.teil_name}
                        </SearchSelectItem>
                    ))}
                </SearchSelect>
            </div>
            <div>
                <LineChart
                    className="h-80"
                    data={sales}
                    index="datum"
                    categories={['Verkaufte Menge']}
                    colors={['indigo', 'rose']}
                    yAxisWidth={60}
                    onValueChange={(v) => console.log(v)}
                />
            </div>
        </>
    );
}