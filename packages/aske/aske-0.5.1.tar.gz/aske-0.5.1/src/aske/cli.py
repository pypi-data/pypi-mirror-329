import click
import os
import subprocess
import sys
import shutil
import time
from aske import __version__
from aske.core.models import (
    GitignoreModel,
    PythonModel,
    NodejsModel,
    NextjsModel,
    ExpressModel,
    RubyModel
)

# Add color constants
RED = "\033[91m"
ORANGE = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def error_text(message):
    """Format error message in red"""
    return f"{RED}{message}{RESET}"

def command_text(message):
    """Format command in orange"""
    return f"{ORANGE}{message}{RESET}"

def success_text(message):
    """Format success message in green"""
    return f"{GREEN}{message}{RESET}"

def change_directory(path):
    """Change directory and return success status"""
    try:
        os.chdir(path)
        return True
    except Exception as e:
        click.echo(f"❌ Error changing directory: {e}", err=True)
        return False

@click.group()
@click.version_option(version=__version__)
def main():
    """ASKE - Platform Architect Development Framework"""
    pass

@main.command()
@click.argument('name')
def python(name):
    """Create a new Python project and set up its structure"""
    project_path = os.path.abspath(name)
    
    # Check if project already exists
    if os.path.exists(project_path):
        click.echo(error_text(f"❌ Error: Project directory '{name}' already exists"), err=True)
        click.echo(error_text("Please choose a different name or remove the existing directory"), err=True)
        sys.exit(1)
    
    click.echo(f"\n🚀 Creating new Python project: {name}")
    click.echo("=" * 50)

    # Create project directory
    click.echo(f"📁 Creating project directory: {project_path}")
    os.makedirs(project_path, exist_ok=False)
    
    # Create virtual environment
    click.echo("\n🔧 Setting up Python virtual environment...")
    
    # Find Python executable
    click.echo("🔍 Looking for Python executable...")
    python_executable = None
    if shutil.which(sys.executable):
        python_executable = sys.executable
        click.echo(f"✓ Using current Python: {python_executable}")
    elif shutil.which('python'):
        python_executable = 'python'
        click.echo("✓ Using 'python' command")
    elif shutil.which('python3'):
        python_executable = 'python3'
        click.echo("✓ Using 'python3' command")
    
    if not python_executable:
        click.echo(error_text("❌ Error: Could not find Python executable"), err=True)
        return

    try:
        venv_path = os.path.join(project_path, "venv")
        subprocess.run([python_executable, "-m", "venv", venv_path], check=True)
        click.echo("✓ Virtual environment created successfully")
    except Exception as e:
        click.echo(error_text(f"❌ Error creating virtual environment: {e}"), err=True)
        return

    # Create project structure
    click.echo("\n✓ Creating project files...")
    files = {
        'requirements.txt': PythonModel.get_requirements(),
        '.env': PythonModel.get_env(name),
        'app.py': PythonModel.get_app(name)
    }

    for file_name, content in files.items():
        full_path = os.path.join(project_path, file_name)
        click.echo(f"📄 Creating {file_name}")
        with open(full_path, 'w') as f:
            f.write(content)

    click.echo("\n✨ Project structure created successfully!")
    click.echo(f"\nTo start working on your project:")
    click.echo(command_text(f"cd {name}"))
    click.echo(command_text("source venv/bin/activate  # On Unix/MacOS"))
    click.echo(command_text("venv\\Scripts\\activate    # On Windows"))
    click.echo(command_text("pip install -r requirements.txt"))
    click.echo(command_text("aske init    # To initialize git and create .gitignore"))

@main.command()
def activate():
    """Activate the Python virtual environment"""
    click.echo("\n🚀 Activating virtual environment...")
    click.echo("=" * 50)

    # Check if we're in a project directory
    venv_path = os.path.join(os.getcwd(), "venv")
    if not os.path.exists(venv_path):
        click.echo(error_text("❌ Error: No virtual environment found in current directory"), err=True)
        click.echo(error_text("Make sure you're in a project directory created with 'aske python <name>'"), err=True)
        return

    # Get the activation script path based on platform
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        activate_cmd = activate_script
    else:  # Unix/MacOS
        activate_script = os.path.join(venv_path, "bin", "activate")
        activate_cmd = f"source {activate_script}"

    # Print the command that needs to be evaluated by the shell
    click.echo(command_text(activate_cmd))
    

@main.command()
def init():
    """Initialize git repository with .gitignore"""
    click.echo("\n🚀 Initializing git repository...")
    
    # Check if git is already initialized
    if os.path.exists('.git'):
        click.echo(error_text("❌ Git repository already exists in this directory"), err=True)
        return

    try:
        # Initialize git repository
        subprocess.run(['git', 'init'], check=True)
        click.echo(success_text("✓ Git repository initialized"))

        # Create or update .gitignore
        click.echo("📄 Creating/updating .gitignore file...")
        with open('.gitignore', 'w') as f:
            f.write(GitignoreModel.get_python_gitignore())
        click.echo(success_text("✓ Created/updated .gitignore file"))

        # Add files to git
        subprocess.run(['git', 'add', '.gitignore'], check=True)
        click.echo(success_text("✓ Added .gitignore to git"))
        
        click.echo("\n✨ Git repository initialized successfully!")
        click.echo("\nNext steps:")
        click.echo(command_text("git add ."))
        click.echo(command_text("git commit -m 'Initial commit'"))

    except subprocess.CalledProcessError as e:
        click.echo(error_text(f"❌ Error initializing git repository: {e}"), err=True)
        return
    except Exception as e:
        click.echo(error_text(f"❌ Unexpected error: {e}"), err=True)
        return

@main.command()
@click.argument('name')
def node(name):
    """Create a new Node.js project and set up its structure"""
    project_path = os.path.abspath(name)
    
    # Check if project already exists
    if os.path.exists(project_path):
        click.echo(error_text(f"❌ Error: Project directory '{name}' already exists"), err=True)
        click.echo(error_text("Please choose a different name or remove the existing directory"), err=True)
        sys.exit(1)
    
    # Check if nvm is installed by looking for .nvm directory
    home = os.path.expanduser("~")
    nvm_dir = os.path.join(home, ".nvm")
    if not os.path.exists(nvm_dir):
        click.echo(error_text("\n❌ NVM (Node Version Manager) is not installed or not found!"))
        click.echo("\nPlease install NVM first:")
        click.echo(command_text("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"))
        click.echo("\nThen restart your terminal and run:")
        click.echo(command_text("nvm install node  # Install latest Node.js version"))
        return

    # Check if yarn is installed
    try:
        subprocess.run(['yarn', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(error_text("\n❌ Yarn package manager is not installed!"))
        click.echo("\nPlease install Yarn first:")
        click.echo(command_text("npm install -g yarn  # Install Yarn globally"))
        click.echo("\nOr if you prefer Homebrew:")
        click.echo(command_text("brew install yarn"))
        return

    click.echo(f"\n🚀 Creating new Node.js project: {name}")
    click.echo("=" * 50)

    # Create project directory and structure
    os.makedirs(project_path)
    for dir_name in ['src/controllers', 'src/models', 'src/routes', 'src/middlewares', 'tests']:
        os.makedirs(os.path.join(project_path, dir_name))

    # Create project files
    files = {
        'package.json': NodejsModel.get_package_json(name),
        '.prettierrc': NodejsModel.get_prettierrc(),
        '.eslintrc': NodejsModel.get_eslintrc(),
        'src/index.js': NodejsModel.get_index_js(),
        '.env': NodejsModel.get_env()
    }

    for file_path, content in files.items():
        full_path = os.path.join(project_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
            click.echo(f"📄 Created {file_path}")

    click.echo("\n✨ Project structure created successfully!")
    click.echo("\nNext steps:")
    click.echo(command_text(f"cd {name}"))
    click.echo(command_text("yarn install  # Install dependencies"))
    click.echo(command_text("yarn dev      # Start development server"))
    click.echo(command_text("aske init     # Initialize git repository"))

@main.command()
@click.argument('name')
def next(name):
    """Create a new Next.js project with TypeScript"""
    project_path = os.path.abspath(name)
    
    # Check if project already exists
    if os.path.exists(project_path):
        click.echo(error_text(f"❌ Error: Project directory '{name}' already exists"), err=True)
        click.echo(error_text("Please choose a different name or remove the existing directory"), err=True)
        sys.exit(1)
    
    # Check if nvm is installed
    home = os.path.expanduser("~")
    nvm_dir = os.path.join(home, ".nvm")
    if not os.path.exists(nvm_dir):
        click.echo(error_text("\n❌ NVM (Node Version Manager) is not installed or not found!"))
        click.echo("\nPlease install NVM first:")
        click.echo(command_text("curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"))
        click.echo("\nThen restart your terminal and run:")
        click.echo(command_text("nvm install node  # Install latest Node.js version"))
        return

    # Check if yarn is installed
    try:
        subprocess.run(['yarn', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo(error_text("\n❌ Yarn package manager is not installed!"))
        click.echo("\nPlease install Yarn first:")
        click.echo(command_text("npm install -g yarn  # Install Yarn globally"))
        click.echo("\nOr if you prefer Homebrew:")
        click.echo(command_text("brew install yarn"))
        return

    click.echo(f"\n🚀 Creating new Next.js project: {name}")
    click.echo("=" * 50)

    try:
        # Create Next.js project with TypeScript
        click.echo("\n📦 Creating Next.js project with TypeScript...")
        subprocess.run([
            'npx', 
            'create-next-app@latest', 
            name, 
            '--typescript', 
            '--use-yarn',
            '--no-git',  # Don't initialize git - we'll use aske init
            '--src-dir',  # Use src directory structure
            '--import-alias', '@/*'  # Modern import alias
        ], check=True)

        # Wait a moment for file system to sync
        time.sleep(1)

        # Create ModelPrompt component
        component_path = os.path.join(project_path, 'src/components/ModelPrompt.tsx')
        os.makedirs(os.path.dirname(component_path), exist_ok=True)
        with open(component_path, 'w') as f:
            f.write(NextjsModel.get_model_prompt_component())
        click.echo("✓ Created ModelPrompt component")

        # Update index page - check both possible locations
        index_paths = [
            os.path.join(project_path, 'src/app/page.tsx'),  # New app directory
            os.path.join(project_path, 'src/pages/index.tsx')  # Traditional pages directory
        ]
        
        index_path = None
        for path in index_paths:
            if os.path.exists(os.path.dirname(path)):
                index_path = path
                break

        if index_path:
            with open(index_path, 'w') as f:
                f.write(NextjsModel.get_index_page())
            click.echo(f"✓ Updated index page at {os.path.relpath(index_path, project_path)}")
        else:
            click.echo(error_text("❌ Could not find index page location"))

        click.echo("\n✨ Next.js project created successfully!")
        click.echo("\nNext steps:")
        click.echo(command_text(f"cd {name}"))
        click.echo(command_text("yarn install     # Install dependencies"))
        click.echo(command_text("yarn dev        # Start development server"))
        click.echo(command_text("aske init       # Initialize git repository"))

    except subprocess.CalledProcessError as e:
        click.echo(error_text(f"\n❌ Error creating Next.js project: {e}"), err=True)
        return
    except Exception as e:
        click.echo(error_text(f"\n❌ Unexpected error: {e}"), err=True)
        return

@main.command()
@click.argument('name')
def express(name):
    """Create a new Express.js API project"""
    project_path = os.path.abspath(name)
    
    # Check if project already exists
    if os.path.exists(project_path):
        click.echo(error_text(f"❌ Error: Project directory '{name}' already exists"), err=True)
        click.echo(error_text("Please choose a different name or remove the existing directory"), err=True)
        sys.exit(1)
    
    # Check for NVM and Yarn (reuse existing checks)
    # ... NVM and Yarn checks ...

    click.echo(f"\n🚀 Creating new Express.js API project: {name}")
    click.echo("=" * 50)

    try:
        # Create project structure
        os.makedirs(project_path)
        
        # Create directory structure
        directories = [
            'src/controllers',
            'src/routes',
            'src/middleware',
            'src/utils',
            'src/models',
            'src/services',
            'tests',
            'logs'
        ]
        
        for dir_name in directories:
            dir_path = os.path.join(project_path, dir_name)
            os.makedirs(dir_path)
            click.echo(f"📁 Created {dir_name}")

        # Create project files
        files = {
            'package.json': ExpressModel.get_package_json(name),
            '.env': ExpressModel.get_env(),
            'src/server.js': ExpressModel.get_server_js(),
            'src/app.js': ExpressModel.get_app_js(),
            'src/routes/index.js': ExpressModel.get_routes_index(),
            'src/routes/health.routes.js': ExpressModel.get_health_routes(),
            'src/routes/user.routes.js': ExpressModel.get_user_routes(),
            'src/controllers/user.controller.js': ExpressModel.get_user_controller(),
            'src/middleware/errorHandler.js': ExpressModel.get_error_handler(),
            'src/utils/logger.js': ExpressModel.get_logger(),
        }

        for file_path, content in files.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            click.echo(f"📄 Created {file_path}")

        click.echo("\n✨ Express.js API project created successfully!")
        click.echo("\nNext steps:")
        click.echo(command_text(f"cd {name}"))
        click.echo(command_text("yarn install     # Install dependencies"))
        click.echo(command_text("yarn dev        # Start development server"))
        click.echo(command_text("aske init       # Initialize git repository"))

    except Exception as e:
        click.echo(error_text(f"\n❌ Unexpected error: {e}"), err=True)
        return

@main.command()
@click.argument('name')
def ruby(name):
    """Create a new Ruby on Rails project"""
    
    # Add warning and confirmation prompt
    click.echo(error_text("\n⚠️  Warning: Installing a Ruby on Rails project may modify system files."))
    click.echo("This process will:")
    click.echo("1. Check and possibly install rbenv")
    click.echo("2. Install Ruby 3.2.0 via rbenv")
    click.echo("3. Install Rails and its dependencies")
    click.echo("4. Modify shell configuration files")
    
    if not click.confirm('\nDo you want to continue?', default=False):
        click.echo("\nOperation cancelled.")
        return
        
    project_path = os.path.abspath(name)
    
    # Check if project already exists
    if os.path.exists(project_path):
        click.echo(error_text(f"❌ Error: Project directory '{name}' already exists"), err=True)
        click.echo(error_text("Please choose a different name or remove the existing directory"), err=True)
        sys.exit(1)
    
    # Check if rbenv is installed and properly configured
    try:
        rbenv_version = subprocess.run(['rbenv', 'version'], capture_output=True, text=True).stdout
        click.echo(f"✓ rbenv detected: {rbenv_version.strip()}")
        
        # Get the active Ruby version from rbenv
        rbenv_ruby_version = rbenv_version.split()[0]  # Get just the version number
        
        # Check if we're actually using rbenv's Ruby
        which_ruby = subprocess.run(['which', 'ruby'], capture_output=True, text=True).stdout.strip()
        ruby_version = subprocess.run(['ruby', '-v'], capture_output=True, text=True).stdout
        
        if '.rbenv/shims/ruby' in which_ruby and rbenv_ruby_version >= "3.2.0":
            click.echo(f"✓ Using rbenv Ruby {rbenv_ruby_version}: {which_ruby}")
        else:
            click.echo(error_text("\n❌ Not using the correct rbenv Ruby version!"))
            click.echo(f"Current Ruby path: {which_ruby}")
            click.echo(f"Current version: {ruby_version.strip()}")
            click.echo("\nPlease set up rbenv Ruby 3.2.0:")
            click.echo(command_text("rbenv install 3.2.0"))
            click.echo(command_text("rbenv global 3.2.0"))
            click.echo(command_text("rbenv rehash"))
            click.echo("\nThen restart your terminal and verify with:")
            click.echo(command_text("rbenv version"))
            click.echo(command_text("which ruby  # Should show .rbenv/shims/ruby"))
            click.echo(command_text("ruby -v    # Should show 3.2.0"))
            return
            
    except FileNotFoundError:
        click.echo(error_text("\n❌ rbenv is not installed!"))
        click.echo("\nPlease install rbenv first:")
        click.echo(command_text("brew install rbenv ruby-build"))
        click.echo(command_text("rbenv init"))
        click.echo("\nFollow the instructions above, then run:")
        click.echo(command_text("rbenv install 3.2.0"))
        click.echo(command_text("rbenv global 3.2.0"))
        return

    # Check if Rails is installed with correct Ruby
    try:
        result = subprocess.run(['rails', '-v'], capture_output=True, text=True)
        if result.returncode == 0 and 'Rails' in result.stdout:
            click.echo(f"✓ Rails detected: {result.stdout.strip()}")
        else:
            click.echo(error_text("\n❌ Rails is not properly installed!"))
            click.echo("\nLet's install Rails:")
            click.echo("\n1. First verify you're using rbenv Ruby:")
            click.echo(command_text("rbenv version"))
            
            click.echo("\n2. Install Rails and update rbenv:")
            click.echo(command_text("gem install rails -v 7.1.0"))
            click.echo(command_text("rbenv rehash  # Make Rails executable available"))
            
            click.echo("\n3. Verify Rails installation:")
            click.echo(command_text("rails -v"))
            return
    except FileNotFoundError:
        click.echo(error_text("\n❌ Rails is not installed!"))
        click.echo("\nPlease install Rails and update rbenv:")
        click.echo(command_text("gem install rails -v 7.1.0"))
        click.echo(command_text("rbenv rehash  # Make Rails executable available"))
        return

    # Check if Bundler is installed
    try:
        bundler_version = subprocess.run(['bundle', '-v'], capture_output=True, text=True).stdout
        click.echo(f"✓ Bundler detected: {bundler_version.strip()}")
    except FileNotFoundError:
        click.echo(error_text("\n❌ Bundler is not installed!"))
        click.echo("\nPlease install Bundler:")
        click.echo(command_text("gem install bundler"))
        return

    # Check if PostgreSQL is installed and running
    try:
        psql_version = subprocess.run(['psql', '--version'], capture_output=True, text=True).stdout
        click.echo(f"✓ PostgreSQL detected: {psql_version.strip()}")
        
        # Check if PostgreSQL service is running
        pg_status = subprocess.run(['brew', 'services', 'list'], capture_output=True, text=True).stdout
        if 'postgresql@14' not in pg_status or 'started' not in pg_status:
            click.echo(error_text("\n⚠️  PostgreSQL service is not running!"))
            click.echo("\nStart PostgreSQL service with:")
            click.echo(command_text("brew services start postgresql@14"))
            click.echo("\nThen wait a few seconds and try again.")
            return
        
        click.echo("✓ PostgreSQL service is running")
        
    except FileNotFoundError:
        click.echo(error_text("\n⚠️  PostgreSQL is not installed!"))
        click.echo("\nPlease install and start PostgreSQL:")
        click.echo(command_text("brew install postgresql@14"))
        click.echo(command_text("brew services start postgresql@14"))
        click.echo("\nThen wait a few seconds and try again.")
        return

    # Check and fix rbenv permissions before creating project
    try:
        rbenv_root = subprocess.run(['rbenv', 'root'], capture_output=True, text=True).stdout.strip()
        click.echo("\n🔧 Checking rbenv permissions...")
        
        # Fix permissions for the entire rbenv directory
        subprocess.run([
            'sudo', 'chown', '-R', os.environ['USER'], rbenv_root
        ], check=True)
        
        # Fix permissions for the gems directory
        gems_dir = os.path.join(rbenv_root, "versions", "3.2.0", "lib", "ruby", "gems")
        if os.path.exists(gems_dir):
            subprocess.run([
                'chmod', '-R', '755', gems_dir
            ], check=True)
            
        click.echo("✓ Fixed rbenv permissions")
        
    except subprocess.CalledProcessError as e:
        click.echo(error_text(f"\n❌ Error fixing permissions: {e}"))
        click.echo("\nPlease run these commands manually:")
        click.echo(command_text(f"sudo chown -R $USER {rbenv_root}"))
        click.echo(command_text(f"chmod -R 755 {gems_dir}"))
        return
    except Exception as e:
        click.echo(error_text(f"\n❌ Unexpected error checking permissions: {e}"))
        return

    click.echo(f"\n🚀 Creating new Ruby on Rails project: {name}")
    click.echo("=" * 50)

    try:
        # Create new Rails project
        click.echo("\n📦 Creating Rails project...")
        env = os.environ.copy()
        env['RBENV_VERSION'] = '3.2.0'  # Set Ruby version for this process
        
        subprocess.run([
            'rails', 'new', name,
            '--database=postgresql',
            '--api',
            '--skip-git',  # We'll use aske init
            '--skip-bundle',  # We'll run bundle install later
            '--rails-version=7.1.0'  # Specify Rails version explicitly
        ], check=True, env=env)

        # Create additional files
        files = {
            'Gemfile': RubyModel.get_gemfile(),
            '.rubocop.yml': RubyModel.get_rubocop(),
            '.rspec': RubyModel.get_rspec(),
            '.env': RubyModel.get_env(),
            'README.md': RubyModel.get_readme(name),
            'config/application.rb': RubyModel.get_application_rb(name)
        }

        for file_path, content in files.items():
            full_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            click.echo(f"📄 Created {file_path}")

        # Install dependencies
        click.echo("\n📦 Installing dependencies...")
        subprocess.run(['bundle', 'install'], cwd=project_path, check=True, env=env)

        # Create a script to set up the environment
        setup_script = '''#!/bin/bash
eval "$(rbenv init -)"
rbenv shell 3.2.0
'''
        setup_script_path = os.path.join(project_path, 'setup.sh')
        with open(setup_script_path, 'w') as f:
            f.write(setup_script)
        os.chmod(setup_script_path, 0o755)  # Make executable

        click.echo("\n✨ Ruby on Rails project created successfully!")
        click.echo("\nNext steps:")
        click.echo(command_text(f"cd {name}"))
        click.echo(command_text("source setup.sh               # Set up Ruby environment"))
        click.echo("\nMake sure PostgreSQL is running:")
        click.echo(command_text("brew services list           # Check PostgreSQL status"))
        click.echo(command_text("brew services start postgresql@14  # Start if needed"))
        click.echo("\nThen set up the database:")
        click.echo(command_text("rails db:create db:migrate   # Setup database"))
        click.echo(command_text("rails server                # Start the server"))
        click.echo(command_text("aske init                  # Initialize git repository"))

    except subprocess.CalledProcessError as e:
        click.echo(error_text(f"\n❌ Error creating Rails project: {e}"), err=True)
        return
    except Exception as e:
        click.echo(error_text(f"\n❌ Unexpected error: {e}"), err=True)
        return

if __name__ == '__main__':
    main()
