#!/usr/bin/env python3

import os
import sys
import json
import shutil
import subprocess
import urllib.request
import urllib.error
import re
from pathlib import Path
from typing import List, Dict, Optional

# Load skills database
SKILLS_DB_PATH = Path(__file__).parent.parent / 'data' / 'all_skills_with_cn.json'
skills_database = []

try:
    with open(SKILLS_DB_PATH, 'r', encoding='utf-8') as f:
        skills_database = json.load(f)
    print(f'✓ Loaded {len(skills_database)} skills from database')
except Exception as error:
    print(f'✗ Failed to load skills database: {error}')
    sys.exit(1)


def search_skills(query: str, limit: int = 10) -> List[Dict]:
    """Search skills by query"""
    lower_query = query.lower()
    results = []

    for skill in skills_database:
        score = 0

        # Search in name (highest priority)
        if skill.get('name') and lower_query in skill['name'].lower():
            score += 10

        # Search in description
        if skill.get('description') and lower_query in skill['description'].lower():
            score += 5

        # Search in author
        if skill.get('author') and lower_query in skill['author'].lower():
            score += 3

        if score > 0:
            results.append({'skill': skill, 'score': score})

    # Sort by score (descending) and stars
    results.sort(key=lambda x: (-x['score'], -(x['skill'].get('stars', 0))))

    return [r['skill'] for r in results[:limit]]


def display_results(skills: List[Dict]) -> None:
    """Display search results"""
    if not skills:
        print('\n❌ No skills found matching your query.\n')
        return

    print(f'\n📦 Found {len(skills)} matching skills:\n')

    for index, skill in enumerate(skills, 1):
        print(f"{index}. {skill['name']} (by {skill['author']})")
        print(f"   ⭐ {skill.get('stars', 0)} stars | 🔀 {skill.get('forks', 0)} forks")
        desc = skill.get('description', '')[:100]
        print(f"   📝 {desc}...")
        print(f"   🔗 {skill['githubUrl']}")
        print('')


def download_file(url: str) -> str:
    """Download file from URL"""
    try:
        with urllib.request.urlopen(url) as response:
            if response.status in (301, 302):
                # Handle redirect
                return download_file(response.headers.get('Location'))

            if response.status != 200:
                raise Exception(f'Failed to download: {response.status}')

            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code in (301, 302):
            return download_file(e.headers.get('Location'))
        raise


def has_command(cmd: str) -> bool:
    """Check if command is available"""
    try:
        subprocess.run([cmd, '--version'], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def extract_skill_path(github_url: str) -> Optional[str]:
    """Extract skill folder path from GitHub URL"""
    match = re.search(r'github\.com/[^/]+/[^/]+/tree/[^/]+/(.+)', github_url)
    return match.group(1) if match else None


def extract_repo_info(github_url: str) -> Optional[Dict]:
    """Extract repo info from GitHub URL"""
    match = re.search(r'github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)', github_url)
    if not match:
        return None

    return {
        'owner': match.group(1),
        'repo': match.group(2),
        'branch': match.group(3),
        'path': match.group(4)
    }


async def install_with_svn(skill: Dict) -> str:
    """Install skill using SVN (preferred method)"""
    repo_info = extract_repo_info(skill['githubUrl'])
    if not repo_info:
        raise ValueError('Invalid GitHub URL format')

    svn_url = f"https://github.com/{repo_info['owner']}/{repo_info['repo']}/trunk/{repo_info['path']}"

    home_dir = Path.home()
    claude_skills_dir = home_dir / '.claude' / 'skills'
    skill_dir = claude_skills_dir / skill['name']

    # Create skills directory if it doesn't exist
    claude_skills_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing skill directory if it exists
    if skill_dir.exists():
        print('   ⚠ Removing existing installation...')
        shutil.rmtree(skill_dir, ignore_errors=True)

    print(f'   Using SVN to download from: {svn_url}')

    try:
        subprocess.run(
            ['svn', 'export', svn_url, str(skill_dir)],
            check=True,
            capture_output=True,
            text=True
        )
        return str(skill_dir)
    except subprocess.CalledProcessError as error:
        raise Exception(f'SVN export failed: {error.stderr}')


async def install_with_sparse_checkout(skill: Dict) -> str:
    """Install skill using Git Sparse Checkout"""
    repo_info = extract_repo_info(skill['githubUrl'])
    if not repo_info:
        raise ValueError('Invalid GitHub URL format')

    home_dir = Path.home()
    claude_skills_dir = home_dir / '.claude' / 'skills'
    temp_dir = claude_skills_dir / f".temp_{skill['name']}_{int(__import__('time').time() * 1000)}"
    skill_dir = claude_skills_dir / skill['name']

    # Create skills directory if it doesn't exist
    claude_skills_dir.mkdir(parents=True, exist_ok=True)

    # Remove existing skill directory if it exists
    if skill_dir.exists():
        print('   ⚠ Removing existing installation...')
        shutil.rmtree(skill_dir, ignore_errors=True)

    print('   Using Git sparse checkout...')

    try:
        # Create temp directory
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=temp_dir, check=True, capture_output=True)

        # Add remote
        repo_url = f"https://github.com/{repo_info['owner']}/{repo_info['repo']}.git"
        subprocess.run(
            ['git', 'remote', 'add', 'origin', repo_url],
            cwd=temp_dir,
            check=True,
            capture_output=True
        )

        # Enable sparse checkout
        subprocess.run(
            ['git', 'config', 'core.sparseCheckout', 'true'],
            cwd=temp_dir,
            check=True,
            capture_output=True
        )

        # Set sparse checkout path
        sparse_checkout_path = temp_dir / '.git' / 'info' / 'sparse-checkout'
        sparse_checkout_path.parent.mkdir(parents=True, exist_ok=True)
        with open(sparse_checkout_path, 'w') as f:
            f.write(f"{repo_info['path']}/*\n")

        # Pull the specific folder
        print(f"   Pulling from branch: {repo_info['branch']}...")
        subprocess.run(
            ['git', 'pull', 'origin', repo_info['branch'], '--depth=1'],
            cwd=temp_dir,
            check=True,
            capture_output=True,
            text=True
        )

        # Move the skill folder to final destination
        downloaded_path = temp_dir / repo_info['path']
        if not downloaded_path.exists():
            raise ValueError(f'Downloaded path not found: {downloaded_path}')

        # Copy to final destination
        downloaded_path.rename(skill_dir)

        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

        return str(skill_dir)
    except subprocess.CalledProcessError as error:
        # Clean up temp directory on error
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f'Sparse checkout failed: {error.stderr}')


async def install_skill_md_only(skill: Dict) -> str:
    """Fallback: Install only SKILL.md file"""
    raw_url = skill['githubUrl'].replace('github.com', 'raw.githubusercontent.com').replace('/tree/', '/')
    skill_md_url = f'{raw_url}/SKILL.md'
    print(f'   Downloading SKILL.md only from: {skill_md_url}')

    content = download_file(skill_md_url)

    home_dir = Path.home()
    claude_skills_dir = home_dir / '.claude' / 'skills'
    skill_dir = claude_skills_dir / skill['name']

    claude_skills_dir.mkdir(parents=True, exist_ok=True)
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_path = skill_dir / 'SKILL.md'
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return str(skill_dir)


def parse_skill_config(content: str) -> Dict:
    """Parse SKILL.md for configuration information"""
    config = {
        'name': '',
        'description': '',
        'usage': '',
        'examples': [],
        'dependencies': []
    }

    # Extract name from header
    name_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if name_match:
        config['name'] = name_match.group(1)

    # Extract description
    desc_match = re.search(r'##?\s+Description\s*\n+([\s\S]+?)(?=\n##|$)', content, re.IGNORECASE)
    if desc_match:
        config['description'] = desc_match.group(1).strip()

    # Extract usage
    usage_match = re.search(r'##?\s+Usage\s*\n+([\s\S]+?)(?=\n##|$)', content, re.IGNORECASE)
    if usage_match:
        config['usage'] = usage_match.group(1).strip()

    # Extract examples
    examples_match = re.search(r'##?\s+Examples?\s*\n+([\s\S]+?)(?=\n##|$)', content, re.IGNORECASE)
    if examples_match:
        examples_text = examples_match.group(1)
        config['examples'] = [e.strip() for e in re.split(r'\n\n+', examples_text) if e.strip()]

    return config


def display_skill_guide(skill: Dict, config: Dict, install_path: str, install_method: str) -> None:
    """Display skill configuration and usage guide"""
    print('\n' + '=' * 80)
    print(f"📖 Configuration & Usage Guide for: {skill['name']}")
    print('=' * 80)

    print('\n📍 Installation Path:')
    print(f'   {install_path}')

    if install_method:
        print('\n🔧 Installation Method:')
        print(f'   {install_method}')

    print('\n📝 Description:')
    desc = skill.get('description') or config.get('description') or 'No description available'
    print(f'   {desc}')

    print('\n👤 Author:')
    print(f"   {skill['author']}")

    print('\n⭐ GitHub Stats:')
    print(f"   Stars: {skill.get('stars', 0)} | Forks: {skill.get('forks', 0)}")
    print(f"   Repository: {skill['githubUrl']}")

    if config.get('usage'):
        print('\n🚀 Usage:')
        for line in config['usage'].split('\n'):
            print(f'   {line}')

    if config.get('examples'):
        print('\n💡 Examples:')
        for i, example in enumerate(config['examples'][:3], 1):
            print(f'\n   Example {i}:')
            for line in example.split('\n'):
                print(f'   {line}')

    print('\n✅ Next Steps:')
    print('   1. Restart Claude Code to load the skill')
    print('   2. Use the skill in your conversations')
    print('   3. Check the SKILL.md file for detailed documentation')

    print('\n' + '=' * 80 + '\n')


async def install_skill(skill: Dict) -> bool:
    """Install skill with automatic method selection"""
    print(f"\n📥 Installing skill: {skill['name']}...")
    print(f"   Source: {skill['githubUrl']}")

    skill_dir = None
    install_method = None

    try:
        # Try methods in order of preference
        if has_command('svn'):
            print('   ✓ SVN detected - using efficient folder download')
            install_method = 'SVN'
            skill_dir = await install_with_svn(skill)
        elif has_command('git'):
            print('   ✓ Git detected - using sparse checkout')
            install_method = 'Git Sparse Checkout'
            skill_dir = await install_with_sparse_checkout(skill)
        else:
            print('   ⚠ Neither SVN nor Git detected - downloading SKILL.md only')
            install_method = 'SKILL.md Only'
            skill_dir = await install_skill_md_only(skill)

        print(f'   ✓ Installed to: {skill_dir}')
        print(f'   ✓ Method used: {install_method}')

        # List installed files
        files = os.listdir(skill_dir)
        print(f"   ✓ Files installed: {', '.join(files)}")

        # Parse SKILL.md content for configuration info
        skill_md_path = Path(skill_dir) / 'SKILL.md'
        config = {'name': skill['name'], 'description': skill['description']}

        if skill_md_path.exists():
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            config = parse_skill_config(content)

        # Display configuration and usage guide
        display_skill_guide(skill, config, str(skill_md_path), install_method)

        return True
    except Exception as error:
        print(f'   ✗ Installation failed: {error}')
        print('\n💡 Troubleshooting tips:')
        print('   - Install SVN for efficient downloads')
        print('   - Ensure Git is installed and accessible')
        print('   - Check your internet connection')
        print(f"   - Verify the GitHub URL is accessible: {skill['githubUrl']}")
        return False


def interactive_mode(query: str) -> None:
    """Interactive mode"""
    results = search_skills(query, 20)
    display_results(results)

    if not results:
        return

    # Output JSON for Claude to process
    output = {
        'query': query,
        'results': [
            {
                'index': index + 1,
                'name': skill['name'],
                'author': skill['author'],
                'description': skill['description'],
                'stars': skill.get('stars', 0),
                'forks': skill.get('forks', 0),
                'githubUrl': skill['githubUrl']
            }
            for index, skill in enumerate(results)
        ]
    }

    print('\n---JSON-OUTPUT---')
    print(json.dumps(output, indent=2, ensure_ascii=False))
    print('---END-JSON-OUTPUT---\n')


async def install_by_index(query: str, index: int) -> bool:
    """Install by index"""
    results = search_skills(query, 20)

    if index < 1 or index > len(results):
        print(f'\n❌ Invalid index. Please choose between 1 and {len(results)}\n')
        return False

    skill = results[index - 1]
    return await install_skill(skill)


async def main() -> None:
    """Main function"""
    args = sys.argv[1:]

    if not args:
        print("""
Skill Manager - Search and Install Claude Code Skills

Usage:
  python index.py search <query>          Search for skills
  python index.py install <query> <index> Install a skill by search index
  python index.py direct <github-url>     Install directly from GitHub URL

Examples:
  python index.py search "python testing"
  python index.py install "python testing" 1
""")
        return

    command = args[0]

    if command == 'search':
        query = ' '.join(args[1:])
        if not query:
            print('❌ Please provide a search query')
            return
        interactive_mode(query)
    elif command == 'install':
        query = ' '.join(args[1:-1])
        try:
            index = int(args[-1])
        except (ValueError, IndexError):
            print('❌ Usage: python index.py install <query> <index>')
            return

        if not query:
            print('❌ Usage: python index.py install <query> <index>')
            return

        await install_by_index(query, index)
    else:
        print(f'❌ Unknown command: {command}')


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())