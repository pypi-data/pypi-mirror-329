import psutil
import typer

from src.cli.menu import Menu
from src.core.cursor_cleaner import CursorCleaner
from src.core.cursor_downloader import CursorDownloader
from src.core.cursor_manager import CursorManager
from src.core.update_disabler import CursorAutoUpdateDisabler
from src.utils.browser_handler import BrowserHandler
from src.utils.console import ConsoleManager


class CursorManagerCLI:
    def __init__(self):
        self.app = typer.Typer(
            help="Cursor Manager CLI",
            no_args_is_help=False,
            invoke_without_command=True
        )
        self.console = ConsoleManager()
        self.cursor_manager = CursorManager()
        self.update_disabler = CursorAutoUpdateDisabler()
        self.menu = Menu(self.console)
        self.downloader = CursorDownloader()
        self.cleaner = CursorCleaner()
        self.browser_handler = BrowserHandler()

        self.app.command(help="Xem phiên bản Cursor")(self.info)
        self.app.command(help="Reset ID và thông tin máy")(self.reset)
        self.app.command(name="tat-update",
                         help="Tắt tự động cập nhật")(self.disable_update)
        self.app.command(
            name="tai",
            help="Tải Cursor v0.44.11"
        )(self.download_v0_44_11)
        self.app.command(name="xoa-cache",
                         help="Xóa cache của Cursor")(self.clear_cache)
        self.app.command(name="kill", help="Tắt tất cả tiến trình Cursor")(
            self.kill_cursor)
        self.app.command(name="reset-tai-khoan", help="Reset thông số tài khoản Cursor")(
            self.reset_account)
        self.app.callback()(self.main)

    def info(self):
        try:
            version = self.cursor_manager.get_version()
            self.console.print_version(version)
        except Exception as e:
            self.console.print_error(str(e))

    def reset(self):
        success = self.cursor_manager.reset_cursor()
        if success:
            self.console.print_success("Reset Cursor thành công!")
        else:
            self.console.print_failure("Reset Cursor thất bại!")

    def disable_update(self):
        success = self.update_disabler.disable_auto_update()
        if success:
            self.console.print_success("Đã tắt tự động cập nhật!")
        else:
            self.console.print_failure("Không thể tắt tự động cập nhật!")

    def download_v0_44_11(self):
        success = self.downloader.download()
        if success:
            self.console.print_success("Tải Cursor v0.44.11 thành công!")
        else:
            self.console.print_failure("Tải Cursor v0.44.11 thất bại!")

    def clear_cache(self):
        success = self.cleaner.clear_cache()
        if success:
            self.console.print_success("Đã xóa cache Cursor!")
        else:
            self.console.print_failure("Không thể xóa cache Cursor!")

    def kill_cursor(self):
        try:
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == 'cursor.exe':
                    try:
                        proc.kill()
                        killed = True
                        self.console.print_success(
                            f"Đã tắt Cursor (PID: {proc.info['pid']})")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        self.console.print_error(
                            f"Không thể tắt Cursor (PID: {proc.info['pid']})")

            if not killed:
                self.console.print_info(
                    "Không tìm thấy tiến trình Cursor nào đang chạy")
        except Exception as e:
            self.console.print_error(f"Lỗi khi tắt Cursor: {str(e)}")

    def reset_account(self):
        success = self.cursor_manager.reset_account()
        if success:
            self.console.print_success("Đã reset thông số tài khoản Cursor!")
            self.browser_handler.open_auth_page()
        else:
            self.console.print_failure("Reset thông số tài khoản thất bại!")

    def show_help(self):
        help_text = {
            "Xem phiên bản Cursor": "Hiển thị phiên bản hiện tại của Cursor",
            "Reset Cursor": "Khởi tạo lại ID máy và thông tin định danh",
            "Tắt tự động cập nhật": "Vô hiệu hóa tính năng tự động cập nhật",
            "Xóa cache": "Dọn dẹp bộ nhớ đệm của Cursor",
            "Tắt Cursor": "Đóng tất cả các tiến trình Cursor đang chạy",
            "Tải Cursor v0.44.11": "Tải về phiên bản Cursor 0.44.11",
            "Reset thông số tài khoản": "Reset thông số tài khoản Cursor",
            "Trợ giúp": "Hiển thị hướng dẫn sử dụng",
            "Thoát": "Thoát khỏi chương trình"
        }

        self.console.print_help_table(help_text)

    def main(self, ctx: typer.Context):
        if ctx.invoked_subcommand is None:
            choices = {
                "Xem phiên bản Cursor": self.info,
                "Reset Cursor": self.reset,
                "Tắt tự động cập nhật": self.disable_update,
                "Xóa cache": self.clear_cache,
                "Tắt Cursor": self.kill_cursor,
                "Reset thông số tài khoản": self.reset_account,
                "Trợ giúp": self.show_help,
                "Thoát": lambda: None
            }

            if self.downloader.should_download():
                choices["Tải Cursor v0.44.11"] = self.download_v0_44_11

            self.menu.show(choices)

    def run(self):
        self.app()


def main():
    console = ConsoleManager()
    cli = CursorManagerCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        console.clear_line()
        console.print_goodbye()


if __name__ == "__main__":
    main()
