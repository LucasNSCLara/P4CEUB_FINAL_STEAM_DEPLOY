import re
from typing import Optional, Dict, Tuple

# GPU Rankings (simplified scoring system)
GPU_RANKINGS = {
    # NVIDIA RTX 40 series
    'rtx 4090': 1000, 'rtx 4080': 950, 'rtx 4070 ti': 900, 'rtx 4070': 850, 'rtx 4060 ti': 800, 'rtx 4060': 750,
    # NVIDIA RTX 30 series
    'rtx 3090 ti': 920, 'rtx 3090': 900, 'rtx 3080 ti': 880, 'rtx 3080': 850, 'rtx 3070 ti': 800, 'rtx 3070': 750,
    'rtx 3060 ti': 700, 'rtx 3060': 650, 'rtx 3050': 550,
    # NVIDIA RTX 20 series
    'rtx 2080 ti': 800, 'rtx 2080': 750, 'rtx 2070': 700, 'rtx 2060': 650,
    # NVIDIA GTX 16 series
    'gtx 1660 ti': 550, 'gtx 1660': 520, 'gtx 1650': 450,
    # NVIDIA GTX 10 series
    'gtx 1080 ti': 750, 'gtx 1080': 700, 'gtx 1070': 650, 'gtx 1060': 550, 'gtx 1050 ti': 400, 'gtx 1050': 350,
    # AMD RX 7000 series
    'rx 7900 xtx': 980, 'rx 7900 xt': 920, 'rx 7800 xt': 850, 'rx 7700 xt': 800, 'rx 7600': 650,
    # AMD RX 6000 series
    'rx 6950 xt': 900, 'rx 6900 xt': 880, 'rx 6800 xt': 850, 'rx 6800': 820, 'rx 6700 xt': 750,
    'rx 6600 xt': 650, 'rx 6600': 600, 'rx 6500 xt': 450,
    # AMD RX 5000 series
    'rx 5700 xt': 700, 'rx 5700': 650, 'rx 5600 xt': 600, 'rx 5500 xt': 500,
    # Intel Arc
    'arc a770': 700, 'arc a750': 650, 'arc a580': 550, 'arc a380': 450,
}

# CPU Rankings (simplified scoring system)
CPU_RANKINGS = {
    # Intel 13th/14th gen
    'i9-14900k': 1000, 'i9-13900k': 980, 'i7-14700k': 900, 'i7-13700k': 880,
    'i5-14600k': 800, 'i5-13600k': 780, 'i5-14400': 700, 'i5-13400': 680,
    'i3-14100': 550, 'i3-13100': 530,
    # Intel 12th gen
    'i9-12900k': 950, 'i7-12700k': 850, 'i5-12600k': 750, 'i5-12400': 650, 'i3-12100': 500,
    # Intel 11th gen
    'i9-11900k': 850, 'i7-11700k': 750, 'i5-11600k': 650, 'i5-11400': 550,
    # Intel 10th gen
    'i9-10900k': 800, 'i7-10700k': 700, 'i5-10600k': 600, 'i5-10400': 500, 'i3-10100': 400,
    # Intel 9th gen and older
    'i9-9900k': 750, 'i7-9700k': 650, 'i7-8700k': 600, 'i5-9600k': 550, 'i5-8400': 450,
    'i7-7700k': 500, 'i5-7600k': 400, 'i7-6700k': 450, 'i5-6600k': 350, 'i3-6100': 250,
    # AMD Ryzen 7000 series
    'ryzen 9 7950x': 1000, 'ryzen 9 7900x': 950, 'ryzen 7 7700x': 850, 'ryzen 5 7600x': 750,
    # AMD Ryzen 5000 series
    'ryzen 9 5950x': 950, 'ryzen 9 5900x': 900, 'ryzen 7 5800x': 800, 'ryzen 7 5700x': 750,
    'ryzen 5 5600x': 700, 'ryzen 5 5600': 680, 'ryzen 5 5500': 650,
    # AMD Ryzen 3000 series
    'ryzen 9 3950x': 850, 'ryzen 9 3900x': 800, 'ryzen 7 3700x': 700, 'ryzen 5 3600': 600,
    # AMD Ryzen 2000 series
    'ryzen 7 2700x': 600, 'ryzen 5 2600': 500,
}

def normalize_gpu_name(gpu: str) -> str:
    """Normalize GPU name for comparison."""
    gpu = gpu.lower().strip()
    # Remove common words
    gpu = re.sub(r'\b(nvidia|amd|intel|geforce|radeon|graphics)\b', '', gpu)
    # Remove extra spaces
    gpu = re.sub(r'\s+', ' ', gpu).strip()
    return gpu

def normalize_cpu_name(cpu: str) -> str:
    """Normalize CPU name for comparison."""
    cpu = cpu.lower().strip()
    # Remove common words
    cpu = re.sub(r'\b(intel|amd|core|processor|cpu)\b', '', cpu)
    # Remove extra spaces
    cpu = re.sub(r'\s+', ' ', cpu).strip()
    return cpu

def get_gpu_score(gpu: str) -> int:
    """Get performance score for a GPU."""
    normalized = normalize_gpu_name(gpu)
    
    # Try exact match first
    for key, score in GPU_RANKINGS.items():
        if key in normalized:
            return score
    
    # Default low score if not found
    return 200

def get_cpu_score(cpu: str) -> int:
    """Get performance score for a CPU."""
    normalized = normalize_cpu_name(cpu)
    
    # Try exact match first
    for key, score in CPU_RANKINGS.items():
        if key in normalized:
            return score
    
    # Default low score if not found
    return 200

def extract_ram_gb(ram_text: str) -> Optional[int]:
    """Extract RAM amount in GB from text."""
    # Look for patterns like "8 GB", "16GB", "8 gb ram"
    match = re.search(r'(\d+)\s*gb', ram_text.lower())
    if match:
        return int(match.group(1))
    return None

def compare_specs(
    user_cpu: str,
    user_gpu: str,
    user_ram: str,
    min_cpu: Optional[str],
    min_gpu: Optional[str],
    min_ram: Optional[str],
    rec_cpu: Optional[str],
    rec_gpu: Optional[str],
    rec_ram: Optional[str]
) -> Dict:
    """
    Compare user specs against game requirements.
    Returns detailed comparison results.
    """
    result = {
        "can_run_minimum": False,
        "can_run_recommended": False,
        "details": {
            "cpu": {"status": "unknown", "message": ""},
            "gpu": {"status": "unknown", "message": ""},
            "ram": {"status": "unknown", "message": ""}
        }
    }
    
    # Parse user specs
    user_cpu_score = get_cpu_score(user_cpu) if user_cpu else 0
    user_gpu_score = get_gpu_score(user_gpu) if user_gpu else 0
    user_ram_gb = int(user_ram) if user_ram.isdigit() else 0
    
    # Check CPU
    cpu_meets_min = False
    cpu_meets_rec = False
    
    if min_cpu:
        min_cpu_score = get_cpu_score(min_cpu)
        cpu_meets_min = user_cpu_score >= min_cpu_score
        result["details"]["cpu"]["min_required"] = min_cpu
        result["details"]["cpu"]["min_score"] = min_cpu_score
    else:
        cpu_meets_min = True  # No requirement specified
    
    if rec_cpu:
        rec_cpu_score = get_cpu_score(rec_cpu)
        cpu_meets_rec = user_cpu_score >= rec_cpu_score
        result["details"]["cpu"]["rec_required"] = rec_cpu
        result["details"]["cpu"]["rec_score"] = rec_cpu_score
    else:
        cpu_meets_rec = cpu_meets_min  # If no rec, use min
    
    result["details"]["cpu"]["user_score"] = user_cpu_score
    result["details"]["cpu"]["meets_minimum"] = cpu_meets_min
    result["details"]["cpu"]["meets_recommended"] = cpu_meets_rec
    
    if cpu_meets_rec:
        result["details"]["cpu"]["status"] = "excellent"
        result["details"]["cpu"]["message"] = f"Seu CPU ({user_cpu}) atende aos requisitos recomendados!"
    elif cpu_meets_min:
        result["details"]["cpu"]["status"] = "good"
        result["details"]["cpu"]["message"] = f"Seu CPU ({user_cpu}) atende aos requisitos mínimos."
    else:
        result["details"]["cpu"]["status"] = "insufficient"
        result["details"]["cpu"]["message"] = f"Seu CPU ({user_cpu}) está abaixo dos requisitos mínimos."
    
    # Check GPU
    gpu_meets_min = False
    gpu_meets_rec = False
    
    if min_gpu:
        min_gpu_score = get_gpu_score(min_gpu)
        gpu_meets_min = user_gpu_score >= min_gpu_score
        result["details"]["gpu"]["min_required"] = min_gpu
        result["details"]["gpu"]["min_score"] = min_gpu_score
    else:
        gpu_meets_min = True
    
    if rec_gpu:
        rec_gpu_score = get_gpu_score(rec_gpu)
        gpu_meets_rec = user_gpu_score >= rec_gpu_score
        result["details"]["gpu"]["rec_required"] = rec_gpu
        result["details"]["gpu"]["rec_score"] = rec_gpu_score
    else:
        gpu_meets_rec = gpu_meets_min
    
    result["details"]["gpu"]["user_score"] = user_gpu_score
    result["details"]["gpu"]["meets_minimum"] = gpu_meets_min
    result["details"]["gpu"]["meets_recommended"] = gpu_meets_rec
    
    if gpu_meets_rec:
        result["details"]["gpu"]["status"] = "excellent"
        result["details"]["gpu"]["message"] = f"Sua GPU ({user_gpu}) atende aos requisitos recomendados!"
    elif gpu_meets_min:
        result["details"]["gpu"]["status"] = "good"
        result["details"]["gpu"]["message"] = f"Sua GPU ({user_gpu}) atende aos requisitos mínimos."
    else:
        result["details"]["gpu"]["status"] = "insufficient"
        result["details"]["gpu"]["message"] = f"Sua GPU ({user_gpu}) está abaixo dos requisitos mínimos."
    
    # Check RAM
    ram_meets_min = False
    ram_meets_rec = False
    
    if min_ram:
        min_ram_gb = extract_ram_gb(min_ram)
        if min_ram_gb:
            ram_meets_min = user_ram_gb >= min_ram_gb
            result["details"]["ram"]["min_required"] = f"{min_ram_gb} GB"
    else:
        ram_meets_min = True
    
    if rec_ram:
        rec_ram_gb = extract_ram_gb(rec_ram)
        if rec_ram_gb:
            ram_meets_rec = user_ram_gb >= rec_ram_gb
            result["details"]["ram"]["rec_required"] = f"{rec_ram_gb} GB"
    else:
        ram_meets_rec = ram_meets_min
    
    result["details"]["ram"]["user_amount"] = f"{user_ram_gb} GB"
    result["details"]["ram"]["meets_minimum"] = ram_meets_min
    result["details"]["ram"]["meets_recommended"] = ram_meets_rec
    
    if ram_meets_rec:
        result["details"]["ram"]["status"] = "excellent"
        result["details"]["ram"]["message"] = f"Sua RAM ({user_ram_gb} GB) atende aos requisitos recomendados!"
    elif ram_meets_min:
        result["details"]["ram"]["status"] = "good"
        result["details"]["ram"]["message"] = f"Sua RAM ({user_ram_gb} GB) atende aos requisitos mínimos."
    else:
        result["details"]["ram"]["status"] = "insufficient"
        result["details"]["ram"]["message"] = f"Sua RAM ({user_ram_gb} GB) está abaixo dos requisitos mínimos."
    
    # Overall results
    result["can_run_minimum"] = cpu_meets_min and gpu_meets_min and ram_meets_min
    result["can_run_recommended"] = cpu_meets_rec and gpu_meets_rec and ram_meets_rec
    
    return result
