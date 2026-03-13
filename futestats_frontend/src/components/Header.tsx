import { BarChart3, Menu, Search, Trophy, UserCircle, Users } from "lucide-react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import SearchBar from "./SearchBar";
import { Drawer, DrawerContent, DrawerHeader, DrawerTitle, DrawerTrigger } from "./ui/drawer";

export default function Header() {
    return (
        <header className="flex items-center justify-between bg-primary py-5 px-5 md:px-10 shadow-xl shadow-indigo-950/20 sticky top-0 z-50">

            {/* |=======| FUTURA LOGO |=======| */}
            <div className="flex items-center space-x-2 cursor-pointer">
                <div className="bg-linear-to-br from-indigo-600 to-primary p-2 rounded-xl shadow-md shadow-indigo-800">
                    <BarChart3 className="text-white" size={24} />
                </div>
                <span className="text-xl font-black tracking-tighter text-white hidden md:flex">FUTESTATS<span className="text-purple-600">.BR</span></span>
            </div>

            <div className="flex items-center gap-10 flex-1 justify-end">
                
                <SearchBar />

                <div className="hidden md:flex items-center gap-10">
                    <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                        <Users size={20} />
                        <span className="hidden md:block text-xl">
                            Times
                        </span>
                    </div>
                    <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                        <Trophy size={20} />
                        <span className="hidden md:block overflow-hidden text-xl">
                            Competições
                        </span>
                    </div>
                    <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer">
                        <BarChart3 size={20} />
                        <span className="hidden md:block text-xl">
                            Rankings
                        </span>
                    </div>
                    <div className="flex gap-2 items-center justify-center text-white/80 hover:text-white transition-all cursor-pointer">
                        <UserCircle size={20} />
                    </div>
                </div>

                <div className="block md:hidden">
                    <Drawer direction="right">
                        <DrawerTrigger asChild>
                            <div className="text-white/80 hover:text-white transition-colors">
                                <Menu size={20} />
                            </div>
                        </DrawerTrigger>

                        <DrawerContent className="bg-azul-escuro border border-azul-acinzentado">
                            <DrawerHeader>
                                <DrawerTitle className="text-white">Menu</DrawerTitle>

                            </DrawerHeader>

                            <div className="flex flex-col gap-10 p-5">
                                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer pb-3 border-b">
                                    <Users size={20} />
                                    <span className="text-xl">
                                        Times
                                    </span>
                                </div>
                                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer pb-3 border-b">
                                    <Trophy size={20} />
                                    <span className="overflow-hidden text-xl">
                                        Competições
                                    </span>
                                </div>
                                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer pb-3 border-b">
                                    <BarChart3 size={20} />
                                    <span className="text-xl">
                                        Rankings
                                    </span>
                                </div>
                                <div className="flex gap-2 items-center text-white/80 hover:text-white transition-all cursor-pointer pb-3 border-b">
                                    <UserCircle size={20} />
                                    <span className="text-xl">
                                        Login
                                    </span>
                                </div>
                            </div>

                        </DrawerContent>

                    </Drawer>
                </div>
                
            </div>

        </header>
    );
}