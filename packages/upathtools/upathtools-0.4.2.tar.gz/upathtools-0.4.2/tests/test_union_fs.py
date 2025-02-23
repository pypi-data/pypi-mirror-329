from __future__ import annotations

from fsspec.implementations.local import LocalFileSystem
from fsspec.implementations.memory import MemoryFileSystem
import pytest

from upathtools.union_fs import UnionFileSystem


@pytest.fixture
def union_fs() -> UnionFileSystem:
    """Create a UnionFileSystem with memory and local backends."""
    mem_fs = MemoryFileSystem()
    local_fs = LocalFileSystem()

    # Create some test files in memory
    mem_fs.mkdirs("memdir", exist_ok=True)
    mem_fs.pipe("test.txt", b"memory content")
    mem_fs.pipe("memdir/nested.txt", b"nested content")

    return UnionFileSystem({
        "memory": mem_fs,
        "file": local_fs,
    })


async def test_root_listing(union_fs: UnionFileSystem):
    """Test listing the root shows available protocols."""
    listing = await union_fs._ls("/")
    assert len(listing) == 2  # noqa: PLR2004
    protocols = {item["name"] for item in listing}
    assert protocols == {"memory://", "file://"}


async def test_protocol_routing(union_fs: UnionFileSystem):
    """Test operations are routed to correct filesystem."""
    # Read from memory fs
    content = await union_fs._cat_file("memory://test.txt")
    assert content == b"memory content"

    # Write to memory fs
    await union_fs._pipe_file("memory://new.txt", b"new content")
    assert await union_fs._cat_file("memory://new.txt") == b"new content"


async def test_nested_paths(union_fs: UnionFileSystem):
    """Test operations on nested paths."""
    listing = await union_fs._ls("memory://memdir")
    assert len(listing) == 1
    assert listing[0]["name"] == "memory://memdir/nested.txt"

    content = await union_fs._cat_file("memory://memdir/nested.txt")
    assert content == b"nested content"


async def test_cross_filesystem_copy(union_fs: UnionFileSystem, tmp_path):
    """Test copying between different filesystems."""
    dest = f"file://{tmp_path}/copied.txt"

    # Copy from memory to local
    await union_fs._cp_file("memory://test.txt", dest)

    # Verify content
    with open(tmp_path / "copied.txt", "rb") as f:  # noqa: PTH123
        assert f.read() == b"memory content"


async def test_invalid_protocol(union_fs: UnionFileSystem):
    """Test error handling for invalid protocols."""
    with pytest.raises(ValueError, match="Invalid or unknown protocol"):
        await union_fs._cat_file("invalid://test.txt")


async def test_directory_operations(union_fs: UnionFileSystem):
    """Test directory operations."""
    # Create directory
    await union_fs._makedirs("memory://newdir/subdir", exist_ok=True)

    # Write file in new directory
    await union_fs._pipe_file("memory://newdir/subdir/file.txt", b"test")

    # List directory
    listing = await union_fs._ls("memory://newdir", detail=False)
    assert "memory://newdir/subdir" in listing

    # Remove directory recursively
    await union_fs._rm("memory://newdir", recursive=True)

    # Verify it's gone
    with pytest.raises(FileNotFoundError):
        await union_fs._ls("memory://newdir")


async def test_file_operations(union_fs: UnionFileSystem):
    """Test basic file operations."""
    # Write
    await union_fs._pipe_file("memory://test2.txt", b"test content")

    # Read
    assert await union_fs._cat_file("memory://test2.txt") == b"test content"

    # Get info
    info = await union_fs._info("memory://test2.txt")
    assert info["type"] == "file"
    assert info["name"] == "memory://test2.txt"

    # Delete
    await union_fs._rm_file("memory://test2.txt")

    # Verify deletion
    with pytest.raises(FileNotFoundError):
        await union_fs._cat_file("memory://test2.txt")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
