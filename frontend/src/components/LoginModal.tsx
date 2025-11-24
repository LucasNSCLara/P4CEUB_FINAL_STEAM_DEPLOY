import React, { useState } from 'react';
import { FaTimes, FaUser, FaEnvelope, FaLock } from 'react-icons/fa';

interface LoginModalProps {
    isOpen: boolean;
    onClose: () => void;
    onLogin: (username: string) => void;
}

const LoginModal: React.FC<LoginModalProps> = ({ isOpen, onClose, onLogin }) => {
    const [activeTab, setActiveTab] = useState<'login' | 'signup'>('login');
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    });

    if (!isOpen) return null;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Simulate login/signup
        const username = activeTab === 'signup' ? formData.name : formData.email.split('@')[0];
        onLogin(username || 'Usuário');
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80 backdrop-blur-sm p-4">
            <div className="bg-[#1a1b26] w-full max-w-md rounded-3xl border border-white border-opacity-10 shadow-2xl overflow-hidden animate-fade-in">
                {/* Header */}
                <div className="flex justify-between items-center p-6 border-b border-white border-opacity-5">
                    <h2 className="text-2xl font-bold text-white">
                        {activeTab === 'login' ? 'Bem-vindo de volta' : 'Criar conta'}
                    </h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors">
                        <FaTimes size={24} />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex p-2 bg-black bg-opacity-20">
                    <button
                        className={`flex-1 py-3 rounded-xl font-bold transition-all ${activeTab === 'login' ? 'bg-game-accent text-black shadow-lg' : 'text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('login')}
                    >
                        Login
                    </button>
                    <button
                        className={`flex-1 py-3 rounded-xl font-bold transition-all ${activeTab === 'signup' ? 'bg-game-accent text-black shadow-lg' : 'text-gray-400 hover:text-white'}`}
                        onClick={() => setActiveTab('signup')}
                    >
                        Cadastro
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-8 space-y-6">
                    {activeTab === 'signup' && (
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-gray-500 uppercase ml-1">Nome</label>
                            <div className="relative">
                                <FaUser className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
                                <input
                                    type="text"
                                    placeholder="Seu nome"
                                    className="w-full bg-black bg-opacity-40 border border-gray-700 rounded-xl py-3 pl-12 pr-4 text-white focus:border-game-accent focus:outline-none transition-colors"
                                    value={formData.name}
                                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                    required={activeTab === 'signup'}
                                />
                            </div>
                        </div>
                    )}

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-gray-500 uppercase ml-1">Email</label>
                        <div className="relative">
                            <FaEnvelope className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
                            <input
                                type="email"
                                placeholder="seu@email.com"
                                className="w-full bg-black bg-opacity-40 border border-gray-700 rounded-xl py-3 pl-12 pr-4 text-white focus:border-game-accent focus:outline-none transition-colors"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-xs font-bold text-gray-500 uppercase ml-1">Senha</label>
                        <div className="relative">
                            <FaLock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-500" />
                            <input
                                type="password"
                                placeholder="••••••••"
                                className="w-full bg-black bg-opacity-40 border border-gray-700 rounded-xl py-3 pl-12 pr-4 text-white focus:border-game-accent focus:outline-none transition-colors"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                required
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-gradient-to-r from-game-accent to-emerald-600 hover:from-game-accent-hover hover:to-emerald-500 text-black font-bold py-4 rounded-xl transition-all transform hover:scale-[1.02] shadow-lg shadow-emerald-900/20 mt-4"
                    >
                        {activeTab === 'login' ? 'Entrar' : 'Cadastrar'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default LoginModal;
