"use client";

import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Info } from "lucide-react";
import TimeGeral from "./TimeGeral";
import TimeTitulos from "./TimeTitulos";

export default function TimeTabs() {

    const [value, setValue] = useState("Geral");

    return(
        <div className="w-full">
            <Tabs defaultValue={value} value={value} onValueChange={setValue} className="w-full">
                <TabsList variant={"line"} className="overflow-x-auto h-full">
                    <TabsTrigger className="text-xl" value="Geral">Geral</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Estatísticas">Estatísticas</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Títulos">Títulos</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Campanhas">Campanhas</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Linha do Tempo">Linha do Tempo</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Rankings">Rankings</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Rivais">Rivais</TabsTrigger>
                    <TabsTrigger className="text-xl" value="Estádios">Estádios</TabsTrigger>
                </TabsList>

                <TabsContent value="Geral">
                    <TimeGeral />
                </TabsContent>

                <TabsContent value="Estatísticas">
                    <p>Conteudo estatísticas</p>
                </TabsContent>

                <TabsContent value="Títulos">
                    <TimeTitulos />
                </TabsContent>

                <TabsContent value="Campanhas">
                    <p>Conteudo campanhas</p>
                </TabsContent>

                <TabsContent value="Linha do Tempo">
                    <p>Conteudo linha do tempo</p>
                </TabsContent>

                <TabsContent value="Rankings">
                    <p>Conteudo rankings</p>
                </TabsContent>

                <TabsContent value="Rivais">
                    <p>Conteudo rivais</p>
                </TabsContent>

                <TabsContent value="Estádios">
                    <p>Conteudo estádios</p>
                </TabsContent>
            </Tabs>
        </div>
    );
}