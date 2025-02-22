from ._main import (
    get_default_template_dir_path,
    parse_args,
    main_logic,
    main,
    move_to_target_dir,
    add_template_args,
    copy_template_dir,
    render_template_dirs,
    render_template_files
)

import logging

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(pathname)s | %(name)s | func: %(funcName)s:%(lineno)s | %(levelname)s | %(message)s",
)