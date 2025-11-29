import { commands, ExtensionContext } from 'vscode';
import { connectToColab } from '../colabConnector';

export function registerCommands(context: ExtensionContext) {
    const connectCommand = commands.registerCommand('vscode-colab-integration.connect', async () => {
        try {
            await connectToColab();
            vscode.window.showInformationMessage('Connected to Google Colab successfully!');
        } catch (error) {
            vscode.window.showErrorMessage('Failed to connect to Google Colab: ' + error.message);
        }
    });

    context.subscriptions.push(connectCommand);
}