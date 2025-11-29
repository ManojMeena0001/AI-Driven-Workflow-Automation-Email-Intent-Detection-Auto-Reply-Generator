import * as vscode from 'vscode';
import { registerCommands } from './commands/index';
import { setupColabConnection } from './colabConnector';

export function activate(context: vscode.ExtensionContext) {
    // Setup connection to Google Colab
    setupColabConnection();

    // Register commands
    registerCommands(context);
}

export function deactivate() {
    // Clean up resources if necessary
}