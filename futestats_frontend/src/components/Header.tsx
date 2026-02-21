import { BarChart3, Search, Trophy, Users } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import SearchBar from "./SearchBar";

export default function Header() {
    return (
        <header className="flex items-center justify-between bg-primary py-5 px-5 md:px-10 shadow-xl shadow-indigo-950/20 sticky top-0 z-50">

            {/* |=======| FUTURA LOGO |=======| */}
            <div className="flex items-center space-x-2 cursor-pointer">
                <div className="bg-gradient-to-br from-indigo-600 to-primary p-2 rounded-xl shadow-md shadow-indigo-800">
                    <BarChart3 className="text-white" size={24} />
                </div>
                <span className="text-xl font-black tracking-tighter text-white">FUTESTATS<span className="text-purple-600">.BR</span></span>
            </div>

            <div className="flex items-center gap-10 flex-1 justify-end">
                
                <SearchBar />

                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                    <Users />
                    <span className="hidden md:block text-2xl">
                        Times
                    </span>
                </div>

                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                    <Trophy />
                    <span className="hidden md:block overflow-hidden text-2xl">
                        Competições
                    </span>
                </div>

                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                    <BarChart3 />
                    <span className="hidden md:block text-2xl">
                        Rankings
                    </span>
                </div>
                
            </div>

        </header>
    );
}