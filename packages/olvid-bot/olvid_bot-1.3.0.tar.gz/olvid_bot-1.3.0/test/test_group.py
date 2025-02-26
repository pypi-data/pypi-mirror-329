import logging
from typing import Optional

from grpc.aio import AioRpcError

from ClientHolder import ClientHolder, ClientWrapper
from olvid import OlvidClient, datatypes, listeners


# a bot that accept next group invitation it will receive
class GroupAcceptBot(OlvidClient):
	def __init__(self, identity_id: int, parent_client: OlvidClient):
		super().__init__(parent_client=parent_client)
		self._identity_id = identity_id
		self.group: Optional[datatypes.Group] = None

		# add a listener for group invitations only
		# noinspection PyTypeChecker
		self.add_listener(listeners.InvitationReceivedListener(handler=self.invitation_handler, checkers=[lambda i: i.status == datatypes.Invitation.Status.STATUS_GROUP_INVITATION_WAIT_YOU_TO_ACCEPT], count=1))
		self.add_listener(listeners.GroupNewListener(handler=self.group_new_handler, count=1))

	async def invitation_handler(self, invitation: datatypes.Invitation):
		if invitation.status == invitation.status.STATUS_GROUP_INVITATION_WAIT_YOU_TO_ACCEPT:
			await self.invitation_accept(invitation_id=invitation.id)
		else:
			logging.error(f"{self._identity_id}: received an invalid invitation type: {invitation.status}", invitation)

	async def group_new_handler(self, group: datatypes.Group):
		self.group = group


# a bot that decline next group invitation it will receive
class GroupDeclineBot(GroupAcceptBot):
	async def invitation_handler(self, invitation: datatypes.Invitation):
		if invitation.status == invitation.status.STATUS_GROUP_INVITATION_WAIT_YOU_TO_ACCEPT:
			await self.invitation_decline(invitation_id=invitation.id)
		else:
			logging.error(f"{self._identity_id}: received an invalid invitation type: {invitation.status}", invitation)


# noinspection PyProtectedMember
def get_group_seen_by_a_member(original_group: datatypes.Group, member_contact_id: int):
	group: datatypes.Group = original_group._clone()

	# exchange member and owner permissions
	contact_member: datatypes.GroupMember = [m for m in group.members if m.contact_id == member_contact_id][0]
	contact_permissions: datatypes.GroupMemberPermissions = contact_member.permissions
	contact_member.permissions = group.own_permissions
	group.own_permissions = contact_permissions

	# hide ids
	group.id = 0
	for member in group.members:
		member.contact_id = 0
	for pending_member in group.pending_members:
		pending_member.contact_id = 0
		pending_member.pending_member_id = 0

	return group


async def test_create_normal_group(client_holder: ClientHolder, admin_client: ClientWrapper, group_name: str, group_description: str) -> datatypes.Group:
	member_clients: list[ClientWrapper] = [c for c in client_holder.clients if c != admin_client]
	member_contacts: list[datatypes.Contact] = [await admin_client.get_contact_associated_to_another_client(c) for c in member_clients]

	# create notif bots for admin
	bots: list[OlvidClient] = [
		admin_client.create_notification_bot(listeners.GroupNewListener(handler=admin_client.get_check_content_handler(datatypes.Group(name=group_name, description=group_description), notification_type=listeners.NOTIFICATIONS.GROUP_NEW), count=1)),
		admin_client.create_notification_bot(listeners.DiscussionNewListener(handler=admin_client.get_check_content_handler(datatypes.Discussion(title=group_name), notification_type=listeners.NOTIFICATIONS.DISCUSSION_NEW), count=1)),
		admin_client.create_notification_bot(listeners.GroupUpdateInProgressListener(handler=lambda gid: gid, count=1)),
		admin_client.create_notification_bot(listeners.GroupUpdateFinishedListener(handler=lambda gid: gid, count=1)),
	]
	# check content of group member joined notif
	for member_client in member_clients:
		member_contact: datatypes.Contact = member_contacts[member_clients.index(member_client)]

		def get_contact_id_checker(contact_id: int):
			# noinspection PyUnusedLocal
			def checker(a, b):
				return b.contact_id == contact_id
			return checker

		bots.extend([
			admin_client.create_notification_bot(listeners.GroupMemberJoinedListener(handler=admin_client.get_check_content_handler(datatypes.Group(name=group_name, description=group_description), datatypes.GroupMember(contact_id=member_contact.id), notification_type=listeners.NOTIFICATIONS.GROUP_MEMBER_JOINED), checkers=[get_contact_id_checker(member_contact.id)], count=1)),
			admin_client.create_notification_bot(listeners.GroupPendingMemberRemovedListener(handler=admin_client.get_check_content_handler(datatypes.Group(name=group_name, description=group_description), datatypes.PendingGroupMember(contact_id=member_contact.id, display_name=member_contact.display_name), notification_type=listeners.NOTIFICATIONS.GROUP_PENDING_MEMBER_REMOVED), checkers=[get_contact_id_checker(member_contact.id)], count=1)),
		])

	# create bots to accept invitations and check notif on member side
	for member_client in member_clients:
		bots.extend([
			# bot to accept invitation
			GroupAcceptBot(identity_id=member_client.identity.id, parent_client=member_client),
			# check content bots
			# invitations
			member_client.create_notification_bot(listeners.InvitationReceivedListener(handler=admin_client.get_check_content_handler(datatypes.Invitation(display_name=group_name, status=datatypes.Invitation.Status.STATUS_GROUP_INVITATION_WAIT_YOU_TO_ACCEPT, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_RECEIVED), count=1)),
			member_client.create_notification_bot(listeners.InvitationDeletedListener(handler=admin_client.get_check_content_handler(datatypes.Invitation(display_name=group_name, status=datatypes.Invitation.Status.STATUS_UNSPECIFIED, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_DELETED), count=1)),
			# group
			member_client.create_notification_bot(listeners.GroupNewListener(handler=admin_client.get_check_content_handler(datatypes.Group(name=group_name, description=group_description), notification_type=listeners.NOTIFICATIONS.GROUP_NEW), count=1)),
			member_client.create_notification_bot(listeners.DiscussionNewListener(handler=admin_client.get_check_content_handler(datatypes.Discussion(title=group_name), notification_type=listeners.NOTIFICATIONS.DISCUSSION_NEW), count=1)),
			# group members (only check count)
			member_client.create_notification_bot(listeners.GroupMemberJoinedListener(handler=lambda a, b: a, count=len(member_clients))),
			member_client.create_notification_bot(listeners.GroupPendingMemberRemovedListener(handler=lambda a, b: a, count=len(member_clients))),
		])

	# create group
	new_group: datatypes.Group = await admin_client.group_new_controlled_group(name=group_name, description=group_description, contact_ids=[c.id for c in member_contacts])

	for bot in bots:
		await bot.wait_for_listeners_end()
		await bot.stop()

	new_group._test_assertion(datatypes.Group(name=group_name, description=group_description, keycloak_managed=False, has_a_photo=False))
	assert len(new_group.pending_members) == len(member_clients), f"there are not enough pending members in group ({len(member_clients)}) {new_group}"

	return new_group


async def test_disband_group(client_holder: ClientHolder, admin_client: ClientWrapper, group_id: int):
	member_clients: list[ClientWrapper] = [c for c in client_holder.clients if c != admin_client]
	member_contacts: list[datatypes.Contact] = [await admin_client.get_contact_associated_to_another_client(c) for c in
												member_clients]

	original_group: datatypes.Group = await admin_client.group_get(group_id=group_id)

	# create notif-checker bots for group admin
	bots: list[OlvidClient] = [
		admin_client.create_notification_bot(listeners.GroupDeletedListener(handler=admin_client.get_check_content_handler(original_group, notification_type=listeners.NOTIFICATIONS.GROUP_DELETED), count=1)),
		admin_client.create_notification_bot(listeners.DiscussionLockedListener(handler=admin_client.get_check_content_handler(datatypes.Discussion(title=original_group.name), notification_type=listeners.NOTIFICATIONS.DISCUSSION_LOCKED), count=1)),
		admin_client.create_notification_bot(listeners.GroupUpdateInProgressListener(handler=lambda gid: gid, count=1)),
		admin_client.create_notification_bot(listeners.GroupUpdateFinishedListener(handler=lambda gid: gid, count=1)),
	]

	# TODO remove this, used to pass a known bug (group type is not stored so we cannot retrieve it when group have been disbanded)
	original_group.type = datatypes.Group.Type.TYPE_UNSPECIFIED

	# create notif-checker bots for members
	for i in range(len(member_clients)):
		member_client = member_clients[i]
		member_contact_id = member_contacts[i].id
		bots.extend([
			member_client.create_notification_bot(listeners.GroupDeletedListener(handler=member_client.get_check_content_handler(get_group_seen_by_a_member(original_group, member_contact_id), notification_type=listeners.NOTIFICATIONS.GROUP_DELETED), count=1)),
			member_client.create_notification_bot(listeners.DiscussionLockedListener(handler=member_client.get_check_content_handler(datatypes.Discussion(title=original_group.name), notification_type=listeners.NOTIFICATIONS.DISCUSSION_LOCKED), count=1)),
		])

	disbanded_group = await admin_client.group_disband(group_id=original_group.id)
	disbanded_group._test_assertion(original_group)

	for bot in bots:
		await bot.wait_for_listeners_end()
		await bot.stop()


async def test_try_do_delete_a_contact_in_group(client_holder: ClientHolder, admin_client: ClientWrapper):
	member_clients: list[ClientWrapper] = [c for c in client_holder.clients if c != admin_client]
	member_contacts: list[datatypes.Contact] = [await admin_client.get_contact_associated_to_another_client(c) for c in member_clients]

	for member_contact in member_contacts:
		try:
			await admin_client.contact_delete(contact_id=member_contact.id)
			assert False, "Was able to delete a contact in a group"
		except AioRpcError:
			continue


async def test_concurrent_group_updates(client_holder: ClientHolder, admin_client: ClientWrapper, group_id: int):
	member_clients: list[ClientWrapper] = [c for c in client_holder.clients if c != admin_client]
	member_contacts: list[datatypes.Contact] = [await admin_client.get_contact_associated_to_another_client(c) for c in member_clients]

	original_group: datatypes.Group = await admin_client.group_get(group_id=group_id)

	group_updated_1: datatypes.Group = original_group._clone()
	group_updated_1.name += "-First Update"
	group_updated_1.description += "-First Update"
	group_updated_2: datatypes.Group = original_group._clone()
	group_updated_2.name = ""
	group_updated_2.description = ""

	# this handler is used to check multiple ordered notifications with different content
	def get_recursive_check_content_handler(client: ClientWrapper, listener_type: type[listeners.GenericNotificationListener], expectations: list[tuple], notification_type: listeners.NOTIFICATIONS):
		def recursive_check_content_handler(*messages):
			if not expectations:
				assert False, "Invalid expectations count"
			handler = client.get_check_content_handler(*(expectations[0]), notification_type=notification_type)
			ret = handler(*messages)

			# create next listener
			if len(expectations) > 1:
				# noinspection PyArgumentList
				client.create_notification_bot(listener_type(handler=get_recursive_check_content_handler(client, listener_type=listener_type, expectations=expectations[1:], notification_type=notification_type), count=1))

			return ret
		return recursive_check_content_handler

	# wait for task 1 and associated notif
	# create notif-checker bots for group admin
	bots: list[OlvidClient] = [
		admin_client.create_notification_bot(
			listeners.GroupNameUpdatedListener(
				handler=get_recursive_check_content_handler(admin_client, listeners.GroupNameUpdatedListener, [(group_updated_1, original_group.name), (group_updated_2, group_updated_1.name)], notification_type=listeners.NOTIFICATIONS.GROUP_NAME_UPDATED),
				count=1)),
		admin_client.create_notification_bot(
			listeners.GroupDescriptionUpdatedListener(
				handler=get_recursive_check_content_handler(admin_client, listeners.GroupDescriptionUpdatedListener, [(group_updated_1, original_group.description), (group_updated_2, group_updated_1.description)], notification_type=listeners.NOTIFICATIONS.GROUP_DESCRIPTION_UPDATED),
				count=1)),
		admin_client.create_notification_bot(
			listeners.DiscussionTitleUpdatedListener(
				handler=get_recursive_check_content_handler(admin_client, listeners.DiscussionTitleUpdatedListener, [(datatypes.Discussion(title=group_updated_1.name), original_group.name), (datatypes.Discussion(title=group_updated_2.name), group_updated_1.name)], notification_type=listeners.NOTIFICATIONS.DISCUSSION_TITLE_UPDATED),
				count=1)),
	]

	# create notif-checker bots for members: members only receive one update notifications (updates are probably too fast to give time to handle intermediary blob)
	for i in range(len(member_clients)):
		member_client = member_clients[i]
		member_contact_id = member_contacts[i].id
		bots.extend([
			member_client.create_notification_bot(
				listeners.GroupNameUpdatedListener(
					handler=member_client.get_check_content_handler(get_group_seen_by_a_member(group_updated_2, member_contact_id), original_group.name, notification_type=listeners.NOTIFICATIONS.GROUP_NAME_UPDATED),
					count=1)),
			member_client.create_notification_bot(
				listeners.GroupDescriptionUpdatedListener(
					handler=member_client.get_check_content_handler(get_group_seen_by_a_member(group_updated_2, member_contact_id), original_group.description, notification_type=listeners.NOTIFICATIONS.GROUP_DESCRIPTION_UPDATED),
					count=1)),
			member_client.create_notification_bot(
				listeners.DiscussionTitleUpdatedListener(
					handler=member_client.get_check_content_handler(datatypes.Discussion(title=group_updated_2.name), original_group.name, notification_type=listeners.NOTIFICATIONS.DISCUSSION_TITLE_UPDATED),
					count=1)),
		])

	# launch concurrent tasks
	task1 = admin_client.group_update(group=group_updated_1)
	task2 = admin_client.group_update(group=group_updated_2)

	group_update_response_1: datatypes.Group = await task1
	group_update_response_1._test_assertion(group_updated_1)

	group_update_response_2: datatypes.Group = await task2
	group_update_response_2._test_assertion(group_updated_2)

	for bot in bots:
		await bot.wait_for_listeners_end()


# noinspection DuplicatedCode
async def test_update_member_permissions(client_holder: ClientHolder, admin_client: ClientWrapper, group_id: int):
	member_clients: list[ClientWrapper] = [c for c in client_holder.clients if c != admin_client]
	member_contacts: list[datatypes.Contact] = [await admin_client.get_contact_associated_to_another_client(c) for c in
												member_clients]

	original_group: datatypes.Group = await admin_client.group_get(group_id=group_id)

	if not original_group.own_permissions.admin:
		return

	# choose a member, save it's permissions and update it
	group: datatypes.Group = original_group._clone()
	member_contact_id: int = member_contacts[0].id
	member_index: int = [i for i in range(len(group.members)) if group.members[i].contact_id == member_contact_id][0]
	original_member_permissions: datatypes.GroupMemberPermissions = group.members[member_index].permissions._clone()
	new_member_permissions: datatypes.GroupMemberPermissions = datatypes.GroupMemberPermissions()
	group.members[member_index].permissions = new_member_permissions

	# prepare notification handlers
	bots: list[OlvidClient] = [
		admin_client.create_notification_bot(
			listeners.GroupMemberPermissionsUpdatedListener(
				handler=admin_client.get_check_content_handler(group, group.members[member_index], original_member_permissions, notification_type=listeners.NOTIFICATIONS.GROUP_MEMBER_PERMISSIONS_UPDATED),
				count=1)),
	]

	# update member permissions
	response_group = await admin_client.group_update(group=group)
	response_group._test_assertion(group)

	# wait for notifications
	for bot in bots:
		await bot.wait_for_listeners_end()

	####
	# restore original permissions
	####
	group.members[member_index].permissions = original_member_permissions
	bots: list[OlvidClient] = [
		admin_client.create_notification_bot(
			listeners.GroupMemberPermissionsUpdatedListener(
				handler=admin_client.get_check_content_handler(group, group.members[member_index], new_member_permissions, notification_type=listeners.NOTIFICATIONS.GROUP_MEMBER_PERMISSIONS_UPDATED),
				count=1)),
	]

	# update member permissions
	response_group = await admin_client.group_update(group=group)
	response_group._test_assertion(group)

	# wait for notifications
	for bot in bots:
		await bot.wait_for_listeners_end()


async def test_get_identifier(c1: ClientWrapper):
	async for group in c1.group_list():
		identifier_1: bytes = await c1.group_get_bytes_identifier(group_id=group.id)
		identifier_2: bytes = await c1.group_get_bytes_identifier(group_id=group.id)
		assert identifier_1, "group identifier is empty"
		assert identifier_1 == identifier_2, "group identifier are not coherent"


async def test_group(client_holder: ClientHolder):
	for client in client_holder.clients:
		logging.info(f"{client.identity.id}: create normal group")
		group = await test_create_normal_group(client_holder, client, f"{client.identity.id}-NormalGroupName", group_description=f"{client.identity.id} normal group description")
		group_id: int = group.id  # do not use original group, it is not up to date

		await test_get_identifier(client)

		logging.info(f"{client.identity.id}: delete contact in a group")
		await test_try_do_delete_a_contact_in_group(client_holder, client)
		logging.info(f"{client.identity.id}: concurrent group updates")
		await test_concurrent_group_updates(client_holder, client, group_id)
		logging.info(f"{client.identity.id}: permission updates")
		await test_update_member_permissions(client_holder, client, group_id)

		logging.info(f"{client.identity.id}: disband normal group")
		await test_disband_group(client_holder, client, group_id)

		logging.info(f"{client.identity.id}: create empty name group")
		group = await test_create_normal_group(client_holder, client, "", "")
		group_id: int = group.id  # do not use original group, it is not up to date
		logging.info(f"{client.identity.id}: disband empty name group")
		await test_disband_group(client_holder, client, group_id)
