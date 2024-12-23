const mongoose = require('mongoose');

const commentSchema = new mongoose.Schema({
    content: {
        type: String,
        required: true
    },
    blog: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Blog',
        required: true
    },
    author: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    parent: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Comment',
        default: null
    },
    path: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Comment'
    }],
    level: {
        type: Number,
        default: 0
    },
    likes: {
        type: Number,
        default: 0
    },
    dislikes: {
        type: Number,
        default: 0
    }
}, {
    timestamps: true
});

// Pre-save middleware to update path and level
commentSchema.pre('save', async function (next) {
    if (this.parent) {
        const parent = await this.constructor.findById(this.parent);
        if (parent) {
            this.path = [...parent.path, parent._id];
            this.level = parent.level + 1;
        }
    } else {
        this.path = [];
        this.level = 0;
    }
    next();
});

// Helper method to get children
commentSchema.methods.getChildren = async function () {
    return await this.constructor.find({ parent: this._id });
};

// Helper method to get ancestors
commentSchema.methods.getAncestors = async function () {
    return await this.constructor.find({ _id: { $in: this.path } });
};

module.exports = mongoose.model('Comment', commentSchema); 