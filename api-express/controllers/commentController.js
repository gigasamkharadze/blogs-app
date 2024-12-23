const Comment = require('../models/Comment');
const Blog = require('../models/Blog');

exports.createComment = async (req, res) => {
    try {
        const { content, parent } = req.body;
        const blogId = req.params.blogId;

        const blog = await Blog.findById(blogId);
        if (!blog) {
            return res.status(404).json({ message: 'Blog not found' });
        }

        const comment = await Comment.create({
            content,
            blog: blogId,
            author: req.user._id,
            parent
        });

        const populatedComment = await Comment.findById(comment._id)
            .populate('author', 'username');

        res.status(201).json(populatedComment);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.getComments = async (req, res) => {
    try {
        const comments = await Comment.find({ blog: req.params.blogId })
            .populate('author', 'username')
            .sort('path');

        res.json({
            results: comments
        });
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.updateComment = async (req, res) => {
    try {
        const comment = await Comment.findById(req.params.commentId);

        if (!comment) {
            return res.status(404).json({ message: 'Comment not found' });
        }

        if (comment.author.toString() !== req.user._id.toString()) {
            return res.status(403).json({ message: 'Not authorized' });
        }

        comment.content = req.body.content;
        await comment.save();

        const updatedComment = await Comment.findById(comment._id)
            .populate('author', 'username');

        res.json(updatedComment);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.deleteComment = async (req, res) => {
    try {
        const comment = await Comment.findById(req.params.commentId);

        if (!comment) {
            return res.status(404).json({ message: 'Comment not found' });
        }

        if (comment.author.toString() !== req.user._id.toString()) {
            return res.status(403).json({ message: 'Not authorized' });
        }

        await comment.deleteOne();
        res.json({ message: 'Comment removed' });
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.likeComment = async (req, res) => {
    try {
        const comment = await Comment.findById(req.params.commentId);
        if (!comment) {
            return res.status(404).json({ message: 'Comment not found' });
        }

        comment.likes += 1;
        await comment.save();

        res.json(comment);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};

exports.dislikeComment = async (req, res) => {
    try {
        const comment = await Comment.findById(req.params.commentId);
        if (!comment) {
            return res.status(404).json({ message: 'Comment not found' });
        }

        comment.dislikes += 1;
        await comment.save();

        res.json(comment);
    } catch (error) {
        res.status(400).json({ message: error.message });
    }
};