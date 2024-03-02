'use client';
import { Button, Card, Textarea } from '@tremor/react';
import React from 'react';

export default function ChatBox() {
    const [value, setValue] = React.useState('');

    return (
        <Card className="mx-auto w-full">
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    alert(value);
                }}
            >
                <div className="flex flex-col gap-2">
                    <label htmlFor="description" className="text-tremor-default text-tremor-content dark:text-dark-tremor-content">
                        Description
                    </label>
                    <Textarea
                        onChange={(e) => setValue(e.target.value)}
                        id="description"
                        placeholder="Start typing here..."
                        rows={6}
                        value={value}
                    />
                </div>
                <div className="mt-6 flex justify-end">
                    <Button type="submit">
                        Submit
                    </Button>
                </div>
            </form>
        </Card>
    );
}