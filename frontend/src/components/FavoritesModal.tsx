import React from 'react';
import { FaTimes, FaHeart, FaStar } from 'react-icons/fa';

interface FavoriteGame {
    id: number;
    name: string;
    background_image?: string;
    rating?: number;
}

interface FavoritesModalProps {
    isOpen: boolean;
    onClose: () => void;
    favorites: FavoriteGame[];
    onRemoveFavorite: (gameId: number) => void;
    onSelectGame: (gameName: string) => void;
}

const FavoritesModal: React.FC<FavoritesModalProps> = ({
    isOpen,
    onClose,
    favorites,
    onRemoveFavorite,
    onSelectGame
}) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80 backdrop-blur-sm p-4">
            <div className="bg-[#1a1b26] w-full max-w-4xl max-h-[80vh] rounded-3xl border border-white border-opacity-10 shadow-2xl overflow-hidden animate-fade-in flex flex-col">
                {/* Header */}
                <div className="flex justify-between items-center p-6 border-b border-white border-opacity-5">
                    <div className="flex items-center gap-3">
                        <FaHeart className="text-game-accent text-2xl" />
                        <h2 className="text-2xl font-bold text-white">Meus Favoritos</h2>
                        <span className="bg-game-accent bg-opacity-20 text-game-accent px-3 py-1 rounded-full text-sm font-bold">
                            {favorites.length}
                        </span>
                    </div>
                    <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
                        <FaTimes size={24} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6">
                    {favorites.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-64 text-center">
                            <FaHeart className="text-6xl text-gray-700 mb-4" />
                            <h3 className="text-xl font-bold text-gray-400 mb-2">Nenhum favorito ainda</h3>
                            <p className="text-gray-500">Comece a favoritar jogos para vê-los aqui!</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {favorites.map((game) => (
                                <div
                                    key={game.id}
                                    className="glass-panel rounded-2xl overflow-hidden group cursor-pointer hover:border-game-accent transition-all duration-300 border border-transparent relative"
                                >
                                    {/* Remove Button */}
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onRemoveFavorite(game.id);
                                        }}
                                        className="absolute top-2 right-2 z-10 bg-red-500 bg-opacity-80 hover:bg-opacity-100 text-white p-2 rounded-full transition-all transform hover:scale-110"
                                        title="Remover dos favoritos"
                                    >
                                        <FaTimes size={14} />
                                    </button>

                                    {/* Game Card */}
                                    <div
                                        onClick={() => {
                                            onSelectGame(game.name);
                                            onClose();
                                        }}
                                    >
                                        {/* Image */}
                                        <div className="relative h-40 overflow-hidden">
                                            {game.background_image ? (
                                                <img
                                                    src={game.background_image}
                                                    alt={game.name}
                                                    className="w-full h-full object-cover transition duration-500 group-hover:scale-110"
                                                />
                                            ) : (
                                                <div className="w-full h-full bg-gray-800 flex items-center justify-center">
                                                    <FaHeart className="text-gray-600 text-4xl" />
                                                </div>
                                            )}
                                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                                        </div>

                                        {/* Info */}
                                        <div className="p-4">
                                            <h3 className="text-white font-bold text-lg mb-2 line-clamp-2" title={game.name}>
                                                {game.name}
                                            </h3>
                                            {game.rating && game.rating > 0 && (
                                                <div className="flex items-center gap-2">
                                                    <FaStar className="text-game-accent" />
                                                    <span className="text-white font-bold">{game.rating}</span>
                                                    <span className="text-gray-500 text-sm">/ 5</span>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FavoritesModal;
