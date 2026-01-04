#!/bin/bash
# install.sh - FlowCube Bot Setup Script

echo "======================================"
echo "FlowCube Bot - Installation Script"
echo "======================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "⚠️  Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Step 1: Updating system packages..."
sudo apt-get update

echo ""
echo "📦 Step 2: Installing Python dependencies..."
sudo apt-get install -y python3-pip python3-dev

echo ""
echo "📦 Step 3: Installing audio packages..."
sudo apt-get install -y espeak festival

echo ""
echo "📦 Step 4: Installing Python packages..."
pip3 install -r requirements.txt

echo ""
echo "📦 Step 5: Setting up SPI for LED control..."
# Enable SPI (required for WS2812B LEDs)
sudo raspi-config nonint do_spi 0

echo ""
echo "📦 Step 6: Adding user to gpio group..."
sudo usermod -a -G gpio $USER

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Reboot your Raspberry Pi: sudo reboot"
echo "2. Wire up your LED strip and speaker"
echo "3. Run the test script: python3 test_hardware.py"
echo "4. Start the bot: python3 server.py"
echo ""
echo "📝 See README.md for wiring instructions"
echo ""