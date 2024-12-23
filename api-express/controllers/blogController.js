const Blog = require('../models/Blog');

exports.getBlogs = async (req, res) => {
    try {
        const blogs = await Blog.find()
            .populate('author', 'username')
            .sort('-createdAt');

        res.json(blogs);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
};

exports.createBlog = async (req, res) => {
    try {
        const { title, content, tags } = req.body;
        const image = req.file ? req.file.path : null;

        if (!image) {
            return res.status(400).json({ message: 'Please upload an image' });
        }

        const blog = await Blog.create({
            title,
            content,
            image,
            tags: tags ? tags.split(',').map(tag => tag.trim()) : [],
            author: req.user._id
        });

        const populatedBlog = await Blog.findById(blog._id)
            .populate('author', 'username');

        res.status(201).json(populatedBlog);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.getBlog = async (req, res) => {
    try {
        const blog = await Blog.findById(req.params.id)
            .populate('author', 'username');

        if (!blog) {
            return res.status(404).json({ message: 'Blog not found' });
        }

        res.json(blog);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.updateBlog = async (req, res) => {
    try {
        let blog = await Blog.findById(req.params.id);

        if (!blog) {
            return res.status(404).json({ message: 'Blog not found' });
        }

        if (blog.author.toString() !== req.user._id.toString()) {
            return res.status(403).json({ message: 'Not authorized' });
        }

        const { title, content, tags } = req.body;
        const image = req.file ? req.file.path : blog.image;

        blog = await Blog.findByIdAndUpdate(
            req.params.id,
            {
                title,
                content,
                image,
                tags: tags ? tags.split(',').map(tag => tag.trim()) : blog.tags
            },
            { new: true }
        ).populate('author', 'username');

        res.json(blog);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.deleteBlog = async (req, res) => {
    try {
        const blog = await Blog.findById(req.params.id);

        if (!blog) {
            return res.status(404).json({ message: 'Blog not found' });
        }

        if (blog.author.toString() !== req.user._id.toString()) {
            return res.status(403).json({ message: 'Not authorized' });
        }

        await blog.deleteOne();
        res.json({ message: 'Blog removed' });
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};