import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchBar from './SearchBar';
import RequirementsCard from './RequirementsCard';
import LoginModal from './LoginModal';
import FavoritesModal from './FavoritesModal';
import { FaGamepad, FaCheckCircle, FaTimesCircle, FaStar, FaClock, FaTrophy, FaUserCircle, FaHeart, FaSignOutAlt } from 'react-icons/fa';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface GameData {
    id: number;
    name: string;
    background_image?: string;
    released?: string;
    rating?: number;
    metacritic?: number;
    playtime?: number;
    parsed_requirements_min?: any;
    parsed_requirements_rec?: any;
    file_size?: string;
    developers?: Array<{ name: string }>;
    similar_games?: Array<{
        id: number;
        name: string;
        background_image?: string;
        rating?: number;
        genres?: Array<{ name: string }>;
    }>;
}

const GameDashboard: React.FC = () => {
    const [game, setGame] = useState<GameData | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [userSpecs, setUserSpecs] = useState({ cpu: '', gpu: '', ram: '' });
    const [canRunResult, setCanRunResult] = useState<{ min: boolean; rec: boolean } | null>(null);

    // Auth State
    const [isLoginOpen, setIsLoginOpen] = useState(false);
    const [user, setUser] = useState<string | null>(null);
    const [showUserMenu, setShowUserMenu] = useState(false);

    // Favorites State
    const [favorites, setFavorites] = useState<Array<{ id: number; name: string; background_image?: string; rating?: number }>>([]);
    const [isFavoritesOpen, setIsFavoritesOpen] = useState(false);

    // Load favorites from localStorage on mount and when user changes
    useEffect(() => {
        if (user) {
            const storedFavorites = localStorage.getItem(`favorites_${user}`);
            if (storedFavorites) {
                setFavorites(JSON.parse(storedFavorites));
            }
        } else {
            setFavorites([]);
        }
    }, [user]);

    const toggleFavorite = () => {
        if (!user) {
            setIsLoginOpen(true);
            return;
        }

        if (!game) return;

        const isFavorited = favorites.some(fav => fav.id === game.id);

        let newFavorites;
        if (isFavorited) {
            newFavorites = favorites.filter(fav => fav.id !== game.id);
        } else {
            newFavorites = [...favorites, {
                id: game.id,
                name: game.name,
                background_image: game.background_image,
                rating: game.rating
            }];
        }

        setFavorites(newFavorites);
        localStorage.setItem(`favorites_${user}`, JSON.stringify(newFavorites));
    };

    const removeFavorite = (gameId: number) => {
        const newFavorites = favorites.filter(fav => fav.id !== gameId);
        setFavorites(newFavorites);
        if (user) {
            localStorage.setItem(`favorites_${user}`, JSON.stringify(newFavorites));
        }
    };

    const handleLogout = () => {
        setUser(null);
        setShowUserMenu(false);
        setFavorites([]);
    };

    const handleSearch = async (term: string) => {
        setLoading(true);
        setError('');
        setGame(null);
        setCanRunResult(null);

        try {
            // Replace with your actual backend URL
            const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
            const response = await axios.get(`${apiUrl}/api/game/${term}`);
            console.log('Game data received:', response.data);
            console.log('Similar games:', response.data.similar_games);
            setGame(response.data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Falha ao buscar dados do jogo. Por favor, tente novamente.');
            console.error('Error fetching game:', err);
        } finally {
            setLoading(false);
        }
    };

    const checkCanRun = () => {
        if (!game) return;
        const hasSpecs = userSpecs.cpu && userSpecs.gpu && userSpecs.ram;
        setCanRunResult({
            min: !!hasSpecs,
            rec: !!hasSpecs && parseInt(userSpecs.ram) >= 16
        });
    };

    const ratingData = {
        labels: ['Avaliação', 'Restante'],
        datasets: [
            {
                data: [game?.rating || 0, 5 - (game?.rating || 0)],
                backgroundColor: ['#00ff9d', 'rgba(255,255,255,0.1)'],
                borderWidth: 0,
                hoverOffset: 4,
            },
        ],
    };

    return (
        <div className="min-h-screen text-white font-sans selection:bg-game-accent selection:text-black">
            <LoginModal
                isOpen={isLoginOpen}
                onClose={() => setIsLoginOpen(false)}
                onLogin={(username) => setUser(username)}
            />

            {/* Background Image Overlay */}
            {game?.background_image && (
                <div className="fixed inset-0 z-0">
                    <div className="absolute inset-0 bg-black bg-opacity-80 z-10"></div>
                    <img src={game.background_image} alt="" className="w-full h-full object-cover blur-sm opacity-40 transform scale-105" />
                </div>
            )}

            <div className="relative z-10 max-w-7xl mx-auto px-4 py-12">
                {/* Auth Button */}
                <div className="absolute top-4 right-4 md:top-8 md:right-8">
                    {user ? (
                        <div className="relative">
                            <button
                                onClick={() => setShowUserMenu(!showUserMenu)}
                                className="flex items-center gap-3 bg-white bg-opacity-10 px-4 py-2 rounded-full border border-white border-opacity-10 backdrop-blur-md hover:bg-opacity-20 transition-all"
                            >
                                <span className="font-bold text-sm">{user}</span>
                                <FaUserCircle className="text-2xl text-game-accent" />
                            </button>

                            {/* User Dropdown Menu */}
                            {showUserMenu && (
                                <div className="absolute right-0 mt-2 w-56 bg-game-card backdrop-blur-xl border border-white/10 rounded-xl overflow-hidden shadow-2xl animate-fade-in">
                                    <button
                                        onClick={() => {
                                            setIsFavoritesOpen(true);
                                            setShowUserMenu(false);
                                        }}
                                        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-white/5 transition-colors text-left"
                                    >
                                        <FaHeart className="text-game-accent" />
                                        <div>
                                            <div className="text-white font-semibold">Meus Favoritos</div>
                                            <div className="text-gray-400 text-xs">{favorites.length} jogos</div>
                                        </div>
                                    </button>
                                    <button
                                        onClick={handleLogout}
                                        className="w-full flex items-center gap-3 px-4 py-3 hover:bg-white/5 transition-colors text-left border-t border-white/5"
                                    >
                                        <FaSignOutAlt className="text-red-400" />
                                        <div className="text-white font-semibold">Sair</div>
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <button
                            onClick={() => setIsLoginOpen(true)}
                            className="bg-game-accent hover:bg-game-accent-hover text-black font-bold py-2 px-6 rounded-full transition-all transform hover:scale-105 shadow-lg shadow-game-accent/20"
                        >
                            Login / Cadastro
                        </button>
                    )}
                </div>

                <header className="text-center mb-16 animate-fade-in mt-12">
                    <h1 className="text-6xl md:text-7xl font-bold mb-6 tracking-tight">
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">Steam</span>
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-game-accent to-game-secondary">Explorer</span>
                    </h1>
                    <p className="text-gray-400 text-xl mb-10 font-light tracking-wide">Análise de Próxima Geração para Gamers PC</p>
                    <SearchBar onSearch={handleSearch} loading={loading} />
                    {error && <p className="text-red-500 mt-6 bg-red-500 bg-opacity-10 py-2 px-4 rounded-lg inline-block">{error}</p>}
                </header>

                {loading && (
                    <div className="flex justify-center my-32">
                        <div className="relative w-24 h-24">
                            <div className="absolute inset-0 border-4 border-game-card rounded-full"></div>
                            <div className="absolute inset-0 border-4 border-game-accent rounded-full border-t-transparent animate-spin"></div>
                        </div>
                    </div>
                )}

                {game && !loading && (
                    <div className="animate-slide-up space-y-12">
                        {/* Hero Section */}
                        <div className="relative rounded-3xl overflow-hidden shadow-2xl group h-[500px] border border-white border-opacity-10">
                            <img
                                src={game.background_image}
                                alt={game.name}
                                className="w-full h-full object-cover transition duration-700 group-hover:scale-105"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-game-dark via-game-dark/80 to-transparent flex flex-col justify-end p-10 md:p-16">
                                {/* Favorite Button */}
                                <button
                                    onClick={toggleFavorite}
                                    className="absolute top-6 right-6 bg-black bg-opacity-60 hover:bg-opacity-80 p-4 rounded-full transition-all transform hover:scale-110 backdrop-blur-sm border border-white border-opacity-10"
                                    title={favorites.some(fav => fav.id === game.id) ? "Remover dos favoritos" : "Adicionar aos favoritos"}
                                >
                                    <FaHeart
                                        className={`text-2xl transition-colors ${favorites.some(fav => fav.id === game.id)
                                            ? 'text-game-accent'
                                            : 'text-gray-400'
                                            }`}
                                    />
                                </button>

                                <div className="flex flex-wrap items-center gap-4 mb-4">
                                    <span className="px-4 py-1.5 bg-white bg-opacity-10 backdrop-blur-md border border-white border-opacity-20 rounded-full text-sm font-bold tracking-wider uppercase">
                                        {game.released?.split('-')[0]}
                                    </span>
                                    {game.metacritic && (
                                        <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-wider uppercase border ${game.metacritic >= 80 ? 'bg-green-500/20 border-green-500 text-green-400' :
                                            game.metacritic >= 60 ? 'bg-yellow-500/20 border-yellow-500 text-yellow-400' : 'bg-red-500/20 border-red-500 text-red-400'
                                            }`}>
                                            Metacritic: {game.metacritic}
                                        </span>
                                    )}
                                </div>
                                <h2 className="text-5xl md:text-7xl font-bold text-white mb-2 drop-shadow-lg">{game.name}</h2>
                            </div>
                        </div>

                        {/* Metrics Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Rating Card */}
                            <div className="glass-panel p-8 rounded-3xl flex flex-col items-center justify-center relative overflow-hidden group">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-game-accent opacity-5 blur-3xl rounded-full group-hover:opacity-10 transition duration-500"></div>
                                <h3 className="text-lg font-bold text-gray-400 mb-6 uppercase tracking-widest flex items-center gap-2">
                                    <FaStar className="text-game-accent" /> Avaliação
                                </h3>
                                <div className="w-40 h-40 relative">
                                    <Doughnut
                                        data={ratingData}
                                        options={{
                                            cutout: '75%',
                                            plugins: { legend: { display: false }, tooltip: { enabled: false } },
                                            animation: { animateScale: true }
                                        }}
                                    />
                                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                                        <span className="text-4xl font-bold text-white">{game.rating}</span>
                                        <span className="text-xs text-gray-500 uppercase font-bold mt-1">de 5</span>
                                    </div>
                                </div>
                            </div>

                            {/* Stats Card */}
                            <div className="glass-panel p-8 rounded-3xl flex flex-col justify-center relative overflow-hidden group">
                                <div className="absolute bottom-0 left-0 w-32 h-32 bg-game-secondary opacity-5 blur-3xl rounded-full group-hover:opacity-10 transition duration-500"></div>
                                <h3 className="text-lg font-bold text-gray-400 mb-8 uppercase tracking-widest flex items-center gap-2">
                                    <FaTrophy className="text-game-secondary" /> Estatísticas
                                </h3>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="text-center p-4 bg-white bg-opacity-5 rounded-2xl border border-white border-opacity-5 hover:border-opacity-10 transition-colors">
                                        <FaClock className="text-3xl text-game-accent mx-auto mb-3" />
                                        <span className="block text-gray-400 text-xs uppercase font-bold mb-1">Tempo de Jogo</span>
                                        <span className="text-2xl font-bold text-white">{game.playtime}h</span>
                                    </div>
                                    <div className="text-center p-4 bg-white bg-opacity-5 rounded-2xl border border-white border-opacity-5 hover:border-opacity-10 transition-colors">
                                        <FaGamepad className="text-3xl text-purple-400 mx-auto mb-3" />
                                        <span className="block text-gray-400 text-xs uppercase font-bold mb-1">Desenvolvedora</span>
                                        <span className="text-sm font-bold text-white truncate max-w-[120px] mx-auto block" title={game.developers?.[0]?.name}>
                                            {game.developers?.[0]?.name || 'N/A'}
                                        </span>
                                    </div>
                                    {game.file_size && (
                                        <div className="col-span-2 text-center p-4 bg-white bg-opacity-5 rounded-2xl border border-white border-opacity-5 hover:border-opacity-10 transition-colors">
                                            <span className="block text-gray-400 text-xs uppercase font-bold mb-1">Tamanho Estimado</span>
                                            <span className="text-xl font-bold text-white">{game.file_size}</span>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Can I Run It Card */}
                            <div className="glass-panel p-8 rounded-3xl relative overflow-hidden">
                                <h3 className="text-lg font-bold text-gray-400 mb-6 uppercase tracking-widest">Roda no meu PC?</h3>
                                <div className="space-y-4">
                                    <div className="space-y-2">
                                        <label className="text-xs font-bold text-gray-500 uppercase ml-1">RAM (GB)</label>
                                        <input
                                            type="text"
                                            placeholder="ex: 16"
                                            className="w-full bg-black bg-opacity-40 border border-gray-700 rounded-xl p-3 text-white focus:border-game-accent focus:outline-none transition-colors"
                                            value={userSpecs.ram}
                                            onChange={(e) => setUserSpecs({ ...userSpecs, ram: e.target.value })}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-xs font-bold text-gray-500 uppercase ml-1">Modelo GPU</label>
                                        <input
                                            type="text"
                                            placeholder="ex: RTX 3060"
                                            className="w-full bg-black bg-opacity-40 border border-gray-700 rounded-xl p-3 text-white focus:border-game-accent focus:outline-none transition-colors"
                                            value={userSpecs.gpu}
                                            onChange={(e) => setUserSpecs({ ...userSpecs, gpu: e.target.value })}
                                        />
                                    </div>
                                    <button
                                        onClick={checkCanRun}
                                        className="w-full bg-gradient-to-r from-game-accent to-emerald-600 hover:from-game-accent-hover hover:to-emerald-500 text-black font-bold py-3.5 rounded-xl transition-all transform hover:scale-[1.02] shadow-lg shadow-emerald-900/20 mt-2"
                                    >
                                        Verificar Compatibilidade
                                    </button>
                                    {canRunResult && (
                                        <div className="grid grid-cols-2 gap-3 mt-4 animate-fade-in">
                                            <div className={`p-3 rounded-xl border flex items-center justify-center gap-2 ${canRunResult.min ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'}`}>
                                                {canRunResult.min ? <FaCheckCircle /> : <FaTimesCircle />} <span className="font-bold text-sm">MÍNIMO</span>
                                            </div>
                                            <div className={`p-3 rounded-xl border flex items-center justify-center gap-2 ${canRunResult.rec ? 'bg-green-500/10 border-green-500/30 text-green-400' : 'bg-red-500/10 border-red-500/30 text-red-400'}`}>
                                                {canRunResult.rec ? <FaCheckCircle /> : <FaTimesCircle />} <span className="font-bold text-sm">RECOMENDADO</span>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* System Requirements Section */}
                        <div className="space-y-8">
                            <h2 className="text-3xl font-bold flex items-center gap-3">
                                <span className="w-1.5 h-8 bg-game-accent rounded-full"></span>
                                Requisitos do Sistema
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                <RequirementsCard
                                    title="Mínimo"
                                    requirements={game.parsed_requirements_min}
                                    type="min"
                                />
                                <RequirementsCard
                                    title="Recomendado"
                                    requirements={game.parsed_requirements_rec}
                                    type="rec"
                                />
                            </div>
                        </div>

                        {/* Intelligent Insight */}
                        <div className="glass-panel p-8 rounded-3xl border-l-4 border-l-game-secondary bg-gradient-to-r from-game-secondary/10 to-transparent">
                            <h3 className="text-xl font-bold mb-3 flex items-center text-white">
                                <span className="text-2xl mr-3">💡</span> Análise de Desempenho
                            </h3>
                            <p className="text-gray-300 leading-relaxed text-lg">
                                {game.parsed_requirements_rec?.gpu
                                    ? `Com base na análise, a GPU recomendada (${game.parsed_requirements_rec.gpu}) oferece aproximadamente 40-60% melhor desempenho para jogos de alta fidelidade em comparação com a especificação mínima. Para jogos em 1440p, sugerimos fortemente atender ao nível recomendado.`
                                    : "Atualize seu hardware para atender às especificações recomendadas para a melhor experiência."}
                            </p>
                        </div>

                        {/* Similar Games Section */}
                        {game.similar_games && game.similar_games.length > 0 && (
                            <div className="space-y-8 pb-12">
                                <h2 className="text-3xl font-bold flex items-center gap-3">
                                    <span className="w-1.5 h-8 bg-game-secondary rounded-full"></span>
                                    Jogos Similares
                                </h2>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    {game.similar_games.map((simGame) => (
                                        <div key={simGame.id} onClick={() => handleSearch(simGame.name)} className="glass-panel rounded-3xl overflow-hidden group cursor-pointer hover:border-game-accent transition-all duration-300 border border-transparent">
                                            <div className="relative h-48 overflow-hidden">
                                                <img
                                                    src={simGame.background_image}
                                                    alt={simGame.name}
                                                    className="w-full h-full object-cover transition duration-500 group-hover:scale-110"
                                                />
                                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                                                <div className="absolute bottom-4 left-4 right-4">
                                                    <h3 className="text-2xl font-bold text-white mb-2">{simGame.name}</h3>
                                                    <div className="flex items-center gap-3 flex-wrap">
                                                        {simGame.genres && simGame.genres.length > 0 && (
                                                            <span className="text-xs font-bold uppercase tracking-wider bg-white/20 px-2 py-1 rounded text-white">
                                                                {simGame.genres[0].name}
                                                            </span>
                                                        )}
                                                        {simGame.rating && simGame.rating > 0 && (
                                                            <div className="flex items-center gap-1 bg-game-accent bg-opacity-20 px-2 py-1 rounded">
                                                                <FaStar className="text-game-accent text-xs" />
                                                                <span className="text-white font-bold text-sm">{simGame.rating}</span>
                                                            </div>
                                                        )}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                    </div>
                )}
            </div>

            {/* Favorites Modal */}
            <FavoritesModal
                isOpen={isFavoritesOpen}
                onClose={() => setIsFavoritesOpen(false)}
                favorites={favorites}
                onRemoveFavorite={removeFavorite}
                onSelectGame={handleSearch}
            />
        </div>
    );
};

export default GameDashboard;
