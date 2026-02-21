"use client";

import { Bar, BarChart, CartesianGrid, Cell, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "../ui/chart";
import { useEffect, useState } from "react";

export default function GraficoResumidoRanking () {

    const [cssVariables, setCssVariables] = useState({
        primary: '#4b2e83', 
        purple: '#a78bfa',
        gray: '#64748b',
        border: '#f1f5f9'
    });

    useEffect(() => {
        const root = document.documentElement;
        const style = getComputedStyle(root);
        
        setCssVariables({
            primary: style.getPropertyValue('--primary').trim() || '#4b2e83',
            purple: '#a78bfa',
            gray: style.getPropertyValue('--muted-foreground').trim() || '#64748b',
            border: style.getPropertyValue('--border').trim() || '#f1f5f9'
        });
    }, []);

    const RANKING_DATA = [
        { name: 'Flamengo', valor: 68 },
        { name: 'Palmeiras', valor: 55 },
        { name: 'Botafogo', valor: 52 },
        { name: 'Bahia', valor: 48 },
        { name: 'Vitória', valor: 45 },
    ];

    const chartConfig = {
        valor: {
            label: "Pontos",
            color: cssVariables.purple,
        },
    };

    return(
        <div className="border rounded-2xl shadow-sm h-full">
            <ChartContainer config={chartConfig} className="w-full h-full">
                <BarChart data={RANKING_DATA} layout="vertical" margin={{ left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke={cssVariables.border} />
                    <XAxis type="number" hide />
                    <YAxis 
                        type="category" 
                        dataKey="name" 
                        axisLine={false} 
                        tickLine={false} 
                        tick={{ fontSize: 13, fontWeight: 900, fill: cssVariables.gray }} 
                        width={100}
                    />
                    <ChartTooltip
                        cursor={{ fill: cssVariables.gray, radius: 10 }}
                        content={<ChartTooltipContent />}
                    />
                    <Bar dataKey="valor" radius={[0, 12, 12, 0]} barSize={40}>
                        {RANKING_DATA.map((entry, index) => (
                            <Cell 
                                key={index} 
                                fill={index === 0 ? `${cssVariables.primary}` : `${chartConfig.valor.color}`} 
                                fillOpacity={1 - (index * 0.15)}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ChartContainer>
        </div>
    )
}