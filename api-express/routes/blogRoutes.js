const express = require('express');
const router = express.Router();
const { protect } = require('../middleware/authMiddleware');
const {
    createBlog,
    getBlogs,
    getBlog,
    updateBlog,
    deleteBlog
} = require('../controllers/blogController');
const upload = require('../middleware/uploadMiddleware');

router.route('/')
    .get(getBlogs)
    .post(protect, upload.single('image'), createBlog);

router.route('/:id')
    .get(getBlog)
    .put(protect, upload.single('image'), updateBlog)
    .delete(protect, deleteBlog);

module.exports = router;