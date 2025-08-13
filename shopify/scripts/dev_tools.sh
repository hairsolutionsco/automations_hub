#!/bin/bash

# Shopify Development Tools Script

echo "🔧 Shopify Development Tools"
echo "============================"

# Check if Shopify CLI is available
if ! command -v shopify &> /dev/null; then
    echo "❌ Shopify CLI not found. Please install it first."
    exit 1
fi

echo "📋 Available Development Commands:"
echo ""
echo "Authentication:"
echo "1. Login to Shopify"
echo "2. Check current user"
echo "3. Logout"
echo ""
echo "App Development:"
echo "4. Create new app"
echo "5. Start app development server"
echo "6. Build app"
echo "7. Deploy app"
echo ""
echo "Theme Development:"
echo "8. Create new theme"
echo "9. Start theme development server"
echo "10. Deploy theme"
echo "11. Pull theme from store"
echo ""
echo "Store Management:"
echo "12. List apps"
echo "13. List themes"
echo "14. Store information"

read -p "Enter your choice (1-14): " choice

case $choice in
    1)
        echo "🔐 Logging in to Shopify..."
        shopify auth login
        ;;
    2)
        echo "👤 Current user:"
        shopify auth list
        ;;
    3)
        echo "🚪 Logging out..."
        shopify auth logout
        ;;
    4)
        echo "📱 Creating new app..."
        read -p "Enter app name: " app_name
        shopify app create "$app_name"
        ;;
    5)
        echo "🚀 Starting app development server..."
        shopify app dev
        ;;
    6)
        echo "🏗️ Building app..."
        shopify app build
        ;;
    7)
        echo "🚀 Deploying app..."
        shopify app deploy
        ;;
    8)
        echo "🎨 Creating new theme..."
        read -p "Enter theme name: " theme_name
        shopify theme init "$theme_name"
        ;;
    9)
        echo "🎨 Starting theme development server..."
        shopify theme dev
        ;;
    10)
        echo "🚀 Deploying theme..."
        shopify theme push
        ;;
    11)
        echo "⬇️ Pulling theme from store..."
        shopify theme pull
        ;;
    12)
        echo "📱 Listing apps..."
        shopify app list
        ;;
    13)
        echo "🎨 Listing themes..."
        shopify theme list
        ;;
    14)
        echo "ℹ️ Store information..."
        shopify app info
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
