class GitLabEvent:

    def __init__(self, name, action, payload):
        self._name: str = name
        self._action: str = action
        self._payload: str = payload

    @property
    def name(self):
        """str: The name of the event"""
        return self._name

    @property
    def action(self):
        """str: The action of the event"""
        return self._action

    @property
    def payload(self):
        """str: The payload of the event"""
        return self._payload


class IssuesClosed(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Issue Hook', 'close', payload)


class IssuesUpdated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Issue Hook', 'update', payload)


class IssuesOpened(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Issue Hook', 'open', payload)


class IssuesReopened(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Issue Hook', 'reopen', payload)


class IssueCommentCreated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('IssueNote Hook', 'create', payload)


class IssueCommentUpdated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('IssueNote Hook', 'update', payload)


class MergeRequestClosed(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'close', payload)


class MergeRequestUpdated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'update', payload)


class MergeRequestOpened(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'open', payload)


class MergeRequestReopened(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'reopen', payload)


class MergeRequestApproved(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'approved', payload)


class MergeRequestUnapproved(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'unapproved', payload)


class MergeRequestApproval(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'approval', payload)


class MergeRequestUnapproval(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'unapproval', payload)


class MergeRequestMerge(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Merge Request Hook', 'merge', payload)


class MergeRequestCommentCreated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('MergeRequestNote Hook', 'create', payload)


class MergeRequestCommentUpdated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('MergeRequestNote Hook', 'update', payload)


class WikiPageCreated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Wiki Page Hook', 'create', payload)


class WikiPageUpdated(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Wiki Page Hook', 'update', payload)


class WikiPageDeleted(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Wiki Page Hook', 'delete', payload)


class Push(GitLabEvent):
    def __init__(self, payload=None):
        super().__init__('Push Hook', '', payload)
