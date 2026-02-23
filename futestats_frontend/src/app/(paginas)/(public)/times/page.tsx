import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ChevronLeft, Share2, Shield } from "lucide-react";
import Image from "next/image";

export default function Times() {
    return(
        <div className="flex flex-col gap-8">
            <div className="flex justify-between">
                <div className="flex items-center gap-2">
                    <Button size={"icon"} variant={"outline"} className="cursor-pointer">
                        <ChevronLeft />
                    </Button>
                    <span className="text-2xl font-semibold">Voltar</span>
                </div>
                <div>
                    <Button size={"icon"} variant={"outline"} className="cursor-pointer">
                        <Share2 />
                    </Button>
                </div>
            </div>

            <div className="relative">
                <div className="h-52 bg-primary rounded-2xl overflow-hidden relative">
                    <div className="absolute top-2 right-0 p-12 opacity-10">
                        <Shield size={200} className="text-white" />
                    </div>
                </div>

                <div className="px-12 -mt-25 relative z-10 flex flex-col md:flex-row md:items-end gap-8">
                    <div className="h-44 w-44 bg-white rounded-2xl p-4 shadow-md shadow-primary/20 border-4 border-white flex items-center justify-center">
                        <Image src="https://picsum.photos/200" width={200} height={200} alt="Time"></Image>
                    </div>

                    <div className="flex-1 flex flex-col gap-0.5">
                        <div className="flex items-center gap-3">
                            <Badge className="bg-amber-100 text-amber-700">Série A</Badge>
                            <div className="flex gap-1">
                                <div className="w-3 h-3 rounded-full border border-white bg-red-500"></div>
                                <div className="w-3 h-3 rounded-full border border-white bg-black"></div>
                            </div>
                        </div>
                        <h1 className="text-5xl font-black text-slate-900 tracking-tighter uppercase">Esporte Clube Vitória</h1>
                        <p className="text-xl font-bold text-primary italic">Leão da Barra</p>
                    </div>
                </div>

                

            </div>

        </div>
    )
}