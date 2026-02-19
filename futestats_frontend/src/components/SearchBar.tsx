import { Search } from "lucide-react";

export default function SearchBar() {
    return (
        <div className="relative group w-full max-w-sm">
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-purple-300 group-focus-within:text-white transition-colors pointer-events-none">
                <Search size={18} />
            </div>

            <input type="search" placeholder="Buscar times, ligas..." 
                className="w-full bg-white/10 border border-white/20 text-white placeholder:text-purple-300/70 text-sm rounded-xl
                py-2.5 pl-11 pr-12 focus:outline-none focus:ring-2 focus:ring-purple-400/50 focus:bg-white/15 transition-all outline-none"
            />
        </div>
    )
}