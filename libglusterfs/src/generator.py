#!/usr/bin/python3

import string

ops = {
	'fgetxattr': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'name', 'const char *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'dict', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'fsetxattr': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'dict', 'dict_t *', 'xattr'),
		('fop-arg', 'flags', 'int32_t', 'flags'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'setxattr': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'dict', 'dict_t *', 'xattr'),
		('fop-arg', 'flags', 'int32_t', 'flags'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'inode-op'),
	),
	'statfs': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'buf', 'struct statvfs *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'fsyncdir': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'flags', 'int32_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'opendir': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'fd', 'fd_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'fstat': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'fsync': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'flags', 'int32_t'),
		('extra', 'preop', 'struct iatt', '&preop'),
		('extra', 'postop', 'struct iatt', '&postop'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'prebuf', 'struct iatt *'),
		('cbk-arg', 'postbuf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'flush': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'writev': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'vector', 'struct iovec *', 'vector'),
		('fop-arg', 'count', 'int32_t'),
		('fop-arg', 'off', 'off_t', 'offset'),
		('fop-arg', 'flags', 'uint32_t', 'flags'),
		('fop-arg', 'iobref', 'struct iobref *'),
		('extra', 'preop', 'struct iatt', '&preop'),
		('extra', 'postop', 'struct iatt', '&postop'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'prebuf', 'struct iatt *'),
		('cbk-arg', 'postbuf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'readv': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'size', 'size_t'),
		('fop-arg', 'offset', 'off_t'),
		('fop-arg', 'flags', 'uint32_t'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'vector', 'struct iovec *'),
		('cbk-arg', 'count', 'int32_t'),
		('cbk-arg', 'stbuf', 'struct iatt *'),
		('cbk-arg', 'iobref', 'struct iobref *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'open': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'flags', 'int32_t'),
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'fd', 'fd_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'create': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'flags', 'int32_t', 'flags'),
		('fop-arg', 'mode', 'mode_t', 'mode'),
		('fop-arg', 'umask', 'mode_t', 'umask', 'nosync'),
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'fd', 'fd_t *'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
		('link', 'loc.inode', '&iatt'),
	),
	'link': (
		('fop-arg', 'oldloc', 'loc_t *', 'loc'),
		('fop-arg', 'newloc', 'loc_t *', 'loc2'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'rename': (
		('fop-arg', 'oldloc', 'loc_t *', 'loc'),
		('fop-arg', 'newloc', 'loc_t *', 'loc2'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preoldparent', 'struct iatt *'),
		('cbk-arg', 'postoldparent', 'struct iatt *'),
		('cbk-arg', 'prenewparent', 'struct iatt *'),
		('cbk-arg', 'postnewparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'symlink': (
		('fop-arg', 'linkpath', 'const char *', 'linkname'),
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'umask', 'mode_t', 'mode', 'nosync'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'rmdir': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'flags', 'int32_t', 'flags'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'unlink': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'flags', 'int32_t', 'flags', 'nosync'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'mkdir': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'mode', 'mode_t', 'mode'),
		('fop-arg', 'umask', 'mode_t', 'umask', 'nosync'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
		('link', 'loc.inode', '&iatt'),
	),
	'mknod': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'mode', 'mode_t', 'mode'),
		('fop-arg', 'rdev', 'dev_t', 'rdev'),
		('fop-arg', 'umask', 'mode_t', 'umask', 'nosync'),
		('extra', 'iatt', 'struct iatt', '&iatt'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'entry-op'),
	),
	'readlink': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'size', 'size_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'path', 'const char *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'access': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'mask', 'int32_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'ftruncate': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'offset', 'off_t', 'offset'),
		('extra', 'preop', 'struct iatt', '&preop'),
		('extra', 'postop', 'struct iatt', '&postop'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'prebuf', 'struct iatt *'),
		('cbk-arg', 'postbuf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'getxattr': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'name', 'const char *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'dict', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'xattrop': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'flags', 'gf_xattrop_flags_t', 'optype'),
		('fop-arg', 'dict', 'dict_t *', 'xattr'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'dict', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'inode-op'),
	),
	'fxattrop': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'flags', 'gf_xattrop_flags_t', 'optype'),
		('fop-arg', 'dict', 'dict_t *', 'xattr'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'dict', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'removexattr': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'name', 'const char *', 'name'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'inode-op'),
	),
	'fremovexattr': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'name', 'const char *', 'name'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'lk': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'cmd', 'int32_t'),
		('fop-arg', 'lock', 'struct gf_flock *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'lock', 'struct gf_flock *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'inodelk': (
		('fop-arg', 'volume', 'const char *'),
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'cmd', 'int32_t'),
		('fop-arg', 'lock', 'struct gf_flock *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'finodelk': (
		('fop-arg', 'volume', 'const char *'),
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'cmd', 'int32_t'),
		('fop-arg', 'lock', 'struct gf_flock *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'entrylk': (
		('fop-arg', 'volume', 'const char *'),
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'basename', 'const char *'),
		('fop-arg', 'cmd', 'entrylk_cmd'),
		('fop-arg', 'type', 'entrylk_type'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'fentrylk': (
		('fop-arg', 'volume', 'const char *'),
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'basename', 'const char *'),
		('fop-arg', 'cmd', 'entrylk_cmd'),
		('fop-arg', 'type', 'entrylk_type'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'rchecksum': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'offset', 'off_t'),
		('fop-arg', 'len', 'int32_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'weak_cksum', 'uint32_t'),
		('cbk-arg', 'strong_cksum', 'uint8_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'readdir': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'size', 'size_t'),
		('fop-arg', 'off', 'off_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'entries', 'gf_dirent_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'readdirp': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'size', 'size_t'),
		('fop-arg', 'off', 'off_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'entries', 'gf_dirent_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'setattr': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'stbuf', 'struct iatt *', 'stat'),
		('fop-arg', 'valid', 'int32_t', 'valid'),
		('extra', 'preop', 'struct iatt', '&preop'),
		('extra', 'postop', 'struct iatt', '&postop'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'statpre', 'struct iatt *'),
		('cbk-arg', 'statpost', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'inode-op'),
	),
	'truncate': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'offset', 'off_t', 'offset'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'prebuf', 'struct iatt *'),
		('cbk-arg', 'postbuf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'inode-op'),
	),
	'stat': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'lookup': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
	),
	'fsetattr': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'stbuf', 'struct iatt *', 'stat'),
		('fop-arg', 'valid', 'int32_t', 'valid'),
		('extra', 'preop', 'struct iatt', '&preop'),
		('extra', 'postop', 'struct iatt', '&postop'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'statpre', 'struct iatt *'),
		('cbk-arg', 'statpost', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'fallocate': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'keep_size', 'int32_t', 'mode'),
		('fop-arg', 'offset', 'off_t', 'offset'),
		('fop-arg', 'len', 'size_t', 'size'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'pre', 'struct iatt *'),
		('cbk-arg', 'post', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'discard': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'offset', 'off_t', 'offset'),
		('fop-arg', 'len', 'size_t', 'size'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'pre', 'struct iatt *'),
		('cbk-arg', 'post', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'zerofill': (
		('fop-arg', 'fd', 'fd_t *', 'fd'),
		('fop-arg', 'offset', 'off_t', 'offset'),
		('fop-arg', 'len', 'off_t', 'size'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'pre', 'struct iatt *'),
		('cbk-arg', 'post', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'ipc': (
		('fop-arg', 'op', 'int32_t'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'xdata', 'dict_t *'),
		('journal', 'fd-op'),
	),
	'seek': (
		('fop-arg', 'fd', 'fd_t *'),
		('fop-arg', 'offset', 'off_t'),
		('fop-arg', 'what', 'gf_seek_what_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'offset', 'off_t'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'getspec': (
		('fop-arg', 'key', 'const char *'),
		('fop-arg', 'flags', 'int32_t'),
		('cbk-arg', 'spec_data', 'char *'),
	),
	'lease': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'lease', 'struct gf_lease *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'lease', 'struct gf_lease *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'getactivelk': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'locklist', 'lock_migration_info_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'setactivelk': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'locklist', 'lock_migration_info_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'put': (
		('fop-arg', 'loc', 'loc_t *', 'loc'),
		('fop-arg', 'mode', 'mode_t', 'mode'),
		('fop-arg', 'umask', 'mode_t', 'umask'),
		('fop-arg', 'flags', 'uint32_t', 'flags'),
		('fop-arg', 'vector', 'struct iovec *', 'vector'),
		('fop-arg', 'count', 'int32_t'),
		('fop-arg', 'off', 'off_t', 'offset'),
		('fop-arg', 'iobref', 'struct iobref *'),
		('fop-arg', 'dict', 'dict_t *', 'xattr'),
		('fop-arg', 'xdata', 'dict_t *', 'xdata'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'preparent', 'struct iatt *'),
		('cbk-arg', 'postparent', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'icreate': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'mode', 'mode_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'inode', 'inode_t *'),
		('cbk-arg', 'buf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'namelink': (
		('fop-arg', 'loc', 'loc_t *'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'prebuf', 'struct iatt *'),
		('cbk-arg', 'postbuf', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
	'copy_file_range': (
		('fop-arg', 'fd_in', 'fd_t *'),
		('fop-arg', 'off_in', 'off64_t '),
		('fop-arg', 'fd_out', 'fd_t *'),
		('fop-arg', 'off_out', 'off64_t '),
		('fop-arg', 'len', 'size_t'),
		('fop-arg', 'flags', 'uint32_t'),
		('fop-arg', 'xdata', 'dict_t *'),
		('cbk-arg', 'stbuf', 'struct iatt *'),
		('cbk-arg', 'prebuf_dst', 'struct iatt *'),
		('cbk-arg', 'postbuf_dst', 'struct iatt *'),
		('cbk-arg', 'xdata', 'dict_t *'),
	),
}

xlator_cbks = {
	'forget': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'inode', 'inode_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'release': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'fd', 'fd_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'releasedir': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'fd', 'fd_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'invalidate': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'inode', 'inode_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'client_destroy': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'client', 'client_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'client_disconnect': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'client', 'client_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'ictxmerge': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'fd', 'fd_t *'),
		('fn-arg', 'inode', 'inode_t *'),
		('fn-arg', 'linked_inode', 'inode_t *'),
		('ret-val', 'void', ''),
	),
}

xlator_dumpops = {
	'priv': (('fn-arg', 'this', 'xlator_t *'), ('ret-val', 'int32_t', '0')),
	'inode': (('fn-arg', 'this', 'xlator_t *'), ('ret-val', 'int32_t', '0')),
	'fd': (('fn-arg', 'this', 'xlator_t *'), ('ret-val', 'int32_t', '0')),
	'inodectx': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'ino', 'inode_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'fdctx': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'fd', 'fd_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'priv_to_dict': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'dict', 'dict_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'inode_to_dict': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'dict', 'dict_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'fd_to_dict': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'dict', 'dict_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'inodectx_to_dict': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'ino', 'inode_t *'),
		('fn-arg', 'dict', 'dict_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'fdctx_to_dict': (
		('fn-arg', 'this', 'xlator_t *'),
		('fn-arg', 'fd', 'fd_t *'),
		('fn-arg', 'dict', 'dict_t *'),
		('ret-val', 'int32_t', '0'),
	),
	'history': (('fn-arg', 'this', 'xlator_t *'), ('ret-val', 'int32_t', '0')),
}

def get_error_arg(type_str):
	return "NULL" if type_str.find(" *") != -1 else "-1"

def get_subs(names, types, cbktypes=None):
	sdict = {"@SHORT_ARGS@": ', '.join(names)}
	# Convert two separate tuples to one of (name, type) sub-tuples.
	as_tuples = list(zip(types, names))
	# Convert each sub-tuple into a "type name" string.
	as_strings = [' '.join(item) for item in as_tuples]
	# Join all of those into one big string.
	sdict["@LONG_ARGS@"] = ',\n\t'.join(as_strings)
	# So much more readable than string.join(map(string.join,zip(...))))
	sdict["@ERROR_ARGS@"] = ', '.join(list(map(get_error_arg, types)))
	if cbktypes is not None:
		sdict["@CBK_ERROR_ARGS@"] = ', '.join(list(map(get_error_arg, cbktypes)))
	return sdict

def generate (tmpl, name, subs):
	text = tmpl.replace("@NAME@", name)
	if name == "writev":
		# More spurious inconsistency.
		text = text.replace("@UPNAME@", "WRITE")
	elif name == "readv":
		text = text.replace("@UPNAME@", "READ")
	else:
		text = text.replace("@UPNAME@", name.upper())
	for old, new in subs[name].items():
		text = text.replace(old, new)
	# TBD: reindent/reformat the result for maximum readability.
	return text

fop_subs = {}
cbk_subs = {}

for name, args in ops.items():

	# Create the necessary substitution strings for fops.
	arg_names = [ a[1] for a in args if a[0] == 'fop-arg']
	arg_types = [ a[2] for a in args if a[0] == 'fop-arg']
	cbk_types = [ a[2] for a in args if a[0] == 'cbk-arg']
	fop_subs[name] = get_subs(arg_names, arg_types, cbk_types)

	# Same thing for callbacks.
	arg_names = [ a[1] for a in args if a[0] == 'cbk-arg']
	arg_types = [ a[2] for a in args if a[0] == 'cbk-arg']
	cbk_subs[name] = get_subs(arg_names, arg_types)

	# Callers can add other subs to these tables, or even create their
	# own tables, using these same techniques, and then pass the result
	# to generate() which would Do The Right Thing with them.
