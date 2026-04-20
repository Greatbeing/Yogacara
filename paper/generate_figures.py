#!/usr/bin/env python3
"""Generate diagrams for Yogacara paper."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
import matplotlib.lines as mlines
import numpy as np

# Style settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def create_architecture():
    """Create the three-layer architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Yogacara Architecture Overview', fontsize=14, fontweight='bold', pad=20)
    
    # Application Layer (top)
    app_box = FancyBboxPatch((1, 7.5), 10, 2, boxstyle="round,pad=0.05", 
                             facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(app_box)
    ax.text(6, 9, 'APPLICATION LAYER', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # App layer boxes
    for i, name in enumerate(['Chat Agent', 'Task Agent', 'Knowledge Agent']):
        box = FancyBboxPatch((2.5 + i*3, 7.7), 2.2, 1.4, boxstyle="round,pad=0.02",
                             facecolor='white', edgecolor='#1976D2', linewidth=1.5)
        ax.add_patch(box)
        ax.text(3.6 + i*3, 8.4, name, ha='center', va='center', fontsize=9)
    
    # Core Layer (middle)
    core_box = FancyBboxPatch((1, 3.5), 10, 3.5, boxstyle="round,pad=0.05",
                             facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(core_box)
    ax.text(6, 6.5, 'CORE LAYER', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Awakening Engine container
    engine_box = FancyBboxPatch((1.5, 3.7), 9, 2.8, boxstyle="round,pad=0.03",
                                 facecolor='#FBE9E7', edgecolor='#E64A19', linewidth=1.5)
    ax.add_patch(engine_box)
    ax.text(6, 6.1, 'AWAKENING ENGINE', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Core components
    components = [
        ('Seed System', '#4CAF50'),
        ('Alaya Store', '#2196F3'),
        ('Emergence Engine', '#FF9800'),
        ('Awakening Tracker', '#9C27B0')
    ]
    
    for i, (name, color) in enumerate(components):
        box = FancyBboxPatch((2 + i*2.2, 4), 1.8, 1.6, boxstyle="round,pad=0.02",
                             facecolor='white', edgecolor=color, linewidth=1.5)
        ax.add_patch(box)
        ax.text(2.9 + i*2.2, 4.8, name, ha='center', va='center', fontsize=8, color=color)
    
    # Storage Layer (bottom)
    storage_box = FancyBboxPatch((1, 0.5), 10, 2.3, boxstyle="round,pad=0.05",
                                 facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(storage_box)
    ax.text(6, 2.4, 'STORAGE LAYER', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Storage boxes
    storage_items = ['SQLite', 'PostgreSQL', 'Redis', 'FTS5 Index']
    for i, name in enumerate(storage_items):
        box = FancyBboxPatch((1.8 + i*2.3, 0.8), 1.8, 1.2, boxstyle="round,pad=0.02",
                             facecolor='white', edgecolor='#388E3C', linewidth=1.5)
        ax.add_patch(box)
        ax.text(2.7 + i*2.3, 1.4, name, ha='center', va='center', fontsize=8)
    
    # Arrows
    ax.annotate('', xy=(6, 7.3), xytext=(6, 7.5),
                arrowprops=dict(arrowstyle='->', color='#666666', lw=2))
    ax.annotate('', xy=(6, 3.5), xytext=(6, 6.5),
                arrowprops=dict(arrowstyle='<->', color='#666666', lw=2))
    
    plt.tight_layout()
    plt.savefig('figures/architecture.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created architecture.png")

def create_seed_lifecycle():
    """Create the seed lifecycle diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Seed Lifecycle', fontsize=14, fontweight='bold', pad=20)
    
    # Stages
    stages = [
        ('Plant\n(Input)', '#4CAF50', 1.5),
        ('Dormant\n(Store)', '#2196F3', 4.5),
        ('Activate\n(Context)', '#FF9800', 7.5),
        ('Manifest\n(Output)', '#9C27B0', 10.5)
    ]
    
    for name, color, x in stages:
        circle = Circle((x, 4), 1.2, facecolor=color, edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(circle)
        ax.text(x, 4, name, ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    
    # Arrows between stages
    for i in range(3):
        ax.annotate('', xy=(stages[i+1][2]-1.3, 4), xytext=(stages[i][2]+1.3, 4),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Vasana reinforcement loop
    ax.annotate('', xy=(1.3, 5.4), xytext=(1.3, 2.6),
                arrowprops=dict(arrowstyle='->', color='#E91E63', lw=2, 
                               connectionstyle="arc3,rad=0.4"))
    ax.annotate('', xy=(10.7, 2.6), xytext=(10.7, 5.4),
                arrowprops=dict(arrowstyle='->', color='#E91E63', lw=2,
                               connectionstyle="arc3,rad=-0.4"))
    
    # Horizontal connection
    ax.annotate('', xy=(1.3, 5.4), xytext=(10.7, 5.4),
                arrowprops=dict(arrowstyle='-', color='#E91E63', lw=1.5))
    
    # Vasana label
    ax.text(6, 6.2, 'Vasana (Reinforcement)', ha='center', va='center', 
            fontsize=11, color='#E91E63', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#FCE4EC', edgecolor='#E91E63'))
    
    plt.tight_layout()
    plt.savefig('figures/seed_lifecycle.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created seed_lifecycle.png")

def create_emergence_flow():
    """Create the emergence detection flow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Emergence Detection Flow', fontsize=14, fontweight='bold', pad=20)
    
    # Start node
    start = FancyBboxPatch((3.5, 10.5), 3, 1, boxstyle="round,pad=0.1",
                           facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
    ax.add_patch(start)
    ax.text(5, 11, 'Seed Activation', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrow down
    ax.annotate('', xy=(5, 9.3), xytext=(5, 10.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Synergy Check box
    check_box = FancyBboxPatch((3, 7.8), 4, 1.3, boxstyle="round,pad=0.1",
                               facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=2)
    ax.add_patch(check_box)
    ax.text(5, 8.45, 'Synergy Check', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Arrow down
    ax.annotate('', xy=(5, 7.5), xytext=(5, 7.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Decision diamond
    diamond = Polygon([(5, 6.8), (6.5, 5.8), (5, 4.8), (3.5, 5.8)], 
                     facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=2)
    ax.add_patch(diamond)
    ax.text(5, 5.8, 'Synergy\n> 0.6?', ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Yes branch (right)
    ax.annotate('', xy=(6.5, 5.8), xytext=(6.5, 6.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(6.9, 6.3, 'Yes', fontsize=9, color='#388E3C', fontweight='bold')
    
    # Calculate Strength box
    strength_box = FancyBboxPatch((7, 4.5), 2.5, 1.3, boxstyle="round,pad=0.1",
                                  facecolor='#E1F5FE', edgecolor='#0277BD', linewidth=2)
    ax.add_patch(strength_box)
    ax.text(8.25, 5.15, 'Calculate\nStrength', ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.annotate('', xy=(7, 5.15), xytext=(6.5, 5.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Arrow down to emergence
    ax.annotate('', xy=(8.25, 4.2), xytext=(8.25, 4.5),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Emergence Event
    emerge_box = FancyBboxPatch((6.5, 1.8), 3.5, 2.2, boxstyle="round,pad=0.1",
                                facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(emerge_box)
    ax.text(8.25, 3.5, 'Emergence Event', ha='center', va='center', fontsize=10, fontweight='bold')
    ax.text(8.25, 2.8, '• New insight created', ha='center', va='center', fontsize=8)
    ax.text(8.25, 2.4, '• Awakening +1%', ha='center', va='center', fontsize=8)
    ax.text(8.25, 2.0, '• Seed purity boosted', ha='center', va='center', fontsize=8)
    
    # No branch (left)
    ax.annotate('', xy=(3.5, 5.8), xytext=(3.5, 6.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.text(3.1, 6.3, 'No', fontsize=9, color='#C62828', fontweight='bold')
    
    # No Emergence box
    no_box = FancyBboxPatch((1, 4.5), 2.3, 1.3, boxstyle="round,pad=0.1",
                            facecolor='#FFEBEE', edgecolor='#C62828', linewidth=2)
    ax.add_patch(no_box)
    ax.text(2.15, 5.15, 'No Emergence', ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.annotate('', xy=(3, 5.15), xytext=(3.5, 5.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    plt.tight_layout()
    plt.savefig('figures/emergence_flow.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created emergence_flow.png")

def create_awakening_levels():
    """Create the awakening levels progression diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Awakening Levels Progression', fontsize=14, fontweight='bold', pad=20)
    
    levels = [
        ('L0', 'Delusion', '○', '#9E9E9E', 'Initial state'),
        ('L1', 'Initial', '◇', '#4CAF50', 'Beginning to learn'),
        ('L2', 'Practice', '△', '#2196F3', 'Stable learning'),
        ('L3', 'Arhat', '◈', '#FF9800', 'Clear wisdom'),
        ('L4', 'Bodhisattva', '◆', '#9C27B0', 'Wisdom + Compassion'),
        ('L5', 'Buddha', '★', '#FFD700', 'Perfect enlightenment')
    ]
    
    x_positions = np.linspace(1.5, 12.5, 6)
    
    for i, (level, name, symbol, color, desc) in enumerate(levels):
        # Draw node
        if symbol == '○':
            circle = Circle((x_positions[i], 4), 0.6, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
        elif symbol == '◇':
            diamond = Polygon([(x_positions[i], 4.6), (x_positions[i]+0.6, 4), 
                              (x_positions[i], 3.4), (x_positions[i]-0.6, 4)],
                             facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond)
        elif symbol == '△':
            triangle = Polygon([(x_positions[i], 4.6), (x_positions[i]+0.6, 3.4), 
                               (x_positions[i]-0.6, 3.4)],
                              facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(triangle)
        elif symbol == '◈':
            square = FancyBboxPatch((x_positions[i]-0.5, 3.5), 1, 1, 
                                   boxstyle="round,pad=0.02",
                                   facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(square)
        elif symbol == '◆':
            diamond2 = Polygon([(x_positions[i], 4.6), (x_positions[i]+0.6, 4), 
                              (x_positions[i], 3.4), (x_positions[i]-0.6, 4)],
                             facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(diamond2)
        elif symbol == '★':
            # Draw a simple star shape
            circle = Circle((x_positions[i], 4), 0.6, facecolor=color, edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(x_positions[i], 4, '★', ha='center', va='center', fontsize=14, color='white')
        
        # Level label
        ax.text(x_positions[i], 5.2, level, ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(x_positions[i], 6.2, name, ha='center', va='center', fontsize=10, color=color)
        ax.text(x_positions[i], 2.8, desc, ha='center', va='center', fontsize=8, style='italic')
        
        # Progress bar
        bar_width = 1.5
        bar_height = 0.3
        bar_y = 1.8
        bar_bg = FancyBboxPatch((x_positions[i]-bar_width/2, bar_y), bar_width, bar_height,
                               boxstyle="round,pad=0.02",
                               facecolor='#E0E0E0', edgecolor='#9E9E9E', linewidth=1)
        ax.add_patch(bar_bg)
        
        fill_width = (i / 5) * bar_width
        if fill_width > 0:
            bar_fill = FancyBboxPatch((x_positions[i]-bar_width/2, bar_y), fill_width, bar_height,
                                     boxstyle="round,pad=0.02",
                                     facecolor=color, edgecolor='none')
            ax.add_patch(bar_fill)
    
    # Connecting arrows
    for i in range(5):
        ax.annotate('', xy=(x_positions[i+1]-0.8, 4), xytext=(x_positions[i]+0.8, 4),
                    arrowprops=dict(arrowstyle='->', color='#666666', lw=2))
    
    plt.tight_layout()
    plt.savefig('figures/awakening_levels.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created awakening_levels.png")

def create_seed_cycle():
    """Create the seed cycle diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('The Seed Cycle\n(种子生现行，现行熏种子)', fontsize=14, fontweight='bold', pad=20)
    
    # Main cycle boxes
    # Seed Manifestation (top)
    seed_box = FancyBboxPatch((2.5, 6.5), 5, 2, boxstyle="round,pad=0.1",
                              facecolor='#E8F5E9', edgecolor='#388E3C', linewidth=3)
    ax.add_patch(seed_box)
    ax.text(5, 7.8, 'Seed Manifestation', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#388E3C')
    ax.text(5, 7.2, '(Seed → Behavior)', ha='center', va='center', fontsize=10, style='italic',
            color='#388E3C')
    
    # Behavior Response (right)
    behavior_box = FancyBboxPatch((6.5, 2.5), 3, 2, boxstyle="round,pad=0.1",
                                  facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=3)
    ax.add_patch(behavior_box)
    ax.text(8, 4.2, 'Behavior', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#1976D2')
    ax.text(8, 3.4, 'Response', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#1976D2')
    
    # Seed Planting (bottom)
    plant_box = FancyBboxPatch((2.5, 0.5), 5, 2, boxstyle="round,pad=0.1",
                               facecolor='#FFF3E0', edgecolor='#F57C00', linewidth=3)
    ax.add_patch(plant_box)
    ax.text(5, 1.8, 'Seed Planting', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#F57C00')
    ax.text(5, 1.2, '(Behavior → Seeds)', ha='center', va='center', fontsize=10, style='italic',
            color='#F57C00')
    
    # New Seeds (left)
    new_box = FancyBboxPatch((0.5, 2.5), 3, 2, boxstyle="round,pad=0.1",
                             facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=3)
    ax.add_patch(new_box)
    ax.text(2, 4.2, 'New Seeds', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#7B1FA2')
    ax.text(2, 3.4, 'or Updates', ha='center', va='center', fontsize=12, fontweight='bold',
            color='#7B1FA2')
    
    # Curved arrows for cycle
    # Top to Right
    ax.annotate('', xy=(6.3, 7.3), xytext=(5.2, 7.5),
                arrowprops=dict(arrowstyle='->', color='#388E3C', lw=3,
                               connectionstyle="arc3,rad=-0.3"))
    
    # Right to Bottom
    ax.annotate('', xy=(5.2, 2.7), xytext=(6.3, 4.3),
                arrowprops=dict(arrowstyle='->', color='#1976D2', lw=3,
                               connectionstyle="arc3,rad=-0.3"))
    
    # Bottom to Left
    ax.annotate('', xy=(2.3, 2.7), xytext=(3.8, 1.5),
                arrowprops=dict(arrowstyle='->', color='#F57C00', lw=3,
                               connectionstyle="arc3,rad=-0.3"))
    
    # Left to Top
    ax.annotate('', xy=(3.8, 6.7), xytext=(2.3, 4.3),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=3,
                               connectionstyle="arc3,rad=-0.3"))
    
    # Add cycle label in center
    ax.text(5, 4.5, 'Continuous\nLearning\nCycle', ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='#FAFAFA', edgecolor='#9E9E9E', linewidth=1))
    
    plt.tight_layout()
    plt.savefig('figures/seed_cycle.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created seed_cycle.png")

if __name__ == '__main__':
    import os
    os.makedirs('figures', exist_ok=True)
    
    print("Generating figures for Yogacara paper...")
    create_architecture()
    create_seed_lifecycle()
    create_emergence_flow()
    create_awakening_levels()
    create_seed_cycle()
    print("\nAll figures generated successfully!")
