import pyperclip
import pyautogui

class Clipboard:
    @staticmethod
    def copy_to_clipboard(text):
        """
        Copia o texto fornecido para a área de transferência do sistema operacional.
        Não interage com nenhuma janela ou campo de texto, apenas atualiza o clipboard.
        """
        pyperclip.copy(text)

    @staticmethod
    def paste_from_clipboard():
        """
        Retorna o conteúdo atual da área de transferência como string.
        Não cola em nenhum campo de texto, apenas lê o clipboard para uso interno no Python.
        """
        return pyperclip.paste()

    @staticmethod
    def paste_hotkey():
        """
        Simula o atalho de teclado Ctrl+V, colando o conteúdo do clipboard
        no campo de texto que estiver com o foco do cursor no sistema operacional.
        Não retorna nada para o Python, apenas executa a ação no sistema.
        """
        pyautogui.hotkey('ctrl', 'v')

    @staticmethod
    def copy_hotkey():
        """
        Simula o atalho de teclado Ctrl+C, copiando o texto selecionado
        no campo de texto ativo do sistema operacional para o clipboard.
        Não retorna nada para o Python, apenas executa a ação no sistema.
        """
        pyautogui.hotkey('ctrl', 'c') 