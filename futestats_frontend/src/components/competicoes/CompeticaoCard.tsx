import { Trophy } from "lucide-react";
import { Button } from "../ui/button";

export default function CompeticaoCard () {
    return(
        <div className="w-75
                        flex flex-col gap-2 border p-3 rounded-2xl shadow-sm">
            <div className="flex items-center gap-2 text-2xl  font-semibold">
                <div className="bg-primary/20 p-2 rounded-xl">
                    <Trophy />
                </div>
                <span className="text-primary">Série A</span>
            </div>
            <div>
                <p className="line-clamp-1">Em busca do título brasileiro</p>
            </div>
            <div className="w-full mt-5">
                <Button className="w-full">Visualizar a competição</Button>
            </div>
        </div>
    )
}