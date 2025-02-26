import copy
import logging

import grpc

from ClientHolder import ClientHolder, ClientWrapper
from olvid import OlvidClient, datatypes, listeners
from utils import send_message_wait_and_check_content


# noinspection PyProtectedMember
async def test_check_list_and_get_content(client_holder: ClientHolder, client1: ClientWrapper, client2: ClientWrapper):
	# check number of contacts is correct
	identity_count = len(client_holder.clients)
	contacts1 = [c async for c in client1.contact_list()]
	assert len(contacts1) == identity_count - 1
	contacts2 = [c async for c in client2.contact_list()]
	assert len(contacts2) == identity_count - 1

	# check contact_lis and contact_get returns same data
	[(await client1.contact_get(contact_id=c.id))._test_assertion(c) for c in contacts1]
	[(await client1.contact_get(contact_id=c.id))._test_assertion(c) for c in contacts1]


# noinspection PyProtectedMember
async def test_down_upgrade_one_to_one_and_locked_discussions(client1: ClientWrapper, client2: ClientWrapper):
	# get other client contact on each side
	contact1: datatypes.Contact = await client1.get_contact_associated_to_another_client(client2)
	contact2: datatypes.Contact = await client2.get_contact_associated_to_another_client(client1)

	if not contact1.has_one_to_one_discussion or not contact2.has_one_to_one_discussion:
		logging.warning(f"test_contact: contacts are not one to one, upgrading channel first ({client1.identity.id} <-> {client2.identity.id})")
		await upgrade_contact_to_one_to_one(client1, client2, contact1, contact2, ideal_discussion1=datatypes.Discussion(title=contact1.display_name), ideal_discussion2=datatypes.Discussion(title=contact2.display_name))

	# get other client discussion on each side
	discussion1: datatypes.Discussion = await client1.get_discussion_associated_to_another_client(client2)
	discussion2: datatypes.Discussion = await client2.get_discussion_associated_to_another_client(client1)

	# send message in discussions to be sure it's not empty
	await send_message_wait_and_check_content(client1, client2, body="Do not let discussion empty")

	# mark as not one to one cause we will use this value to check notif content
	contact1.has_one_to_one_discussion = False
	contact2.has_one_to_one_discussion = False

	# create bot to check contact deletion
	bots: list[OlvidClient] = [
		# contact deleted on each side
		client1.create_notification_bot(listeners.ContactDeletedListener(handler=client1.get_check_content_handler(contact1, notification_type=listeners.NOTIFICATIONS.CONTACT_DELETED), count=1)),
		client2.create_notification_bot(listeners.ContactDeletedListener(handler=client2.get_check_content_handler(contact2, notification_type=listeners.NOTIFICATIONS.CONTACT_DELETED), count=1)),
		# discussion locked on each side
		client1.create_notification_bot(listeners.DiscussionLockedListener(handler=client1.get_check_content_handler(discussion1, notification_type=listeners.NOTIFICATIONS.DISCUSSION_LOCKED), count=1)),
		client2.create_notification_bot(listeners.DiscussionLockedListener(handler=client2.get_check_content_handler(discussion2, notification_type=listeners.NOTIFICATIONS.DISCUSSION_LOCKED), count=1)),
	]

	# delete contact (downgrade to not one to one discussion)
	await client1.contact_downgrade_one_to_one_discussion(contact_id=contact1.id)

	# wait for notifications
	for bot in bots:
		await bot.wait_for_listeners_end()
		await bot.stop()

	# check contacts are still here and have been downgraded
	contact1._test_assertion(await client1.contact_get(contact1.id))
	contact2._test_assertion(await client2.contact_get(contact2.id))

	# check discussion appear as locked
	assert len([ld async for ld in client1.discussion_locked_list() if ld.id == discussion1.id]) == 1, "locked discussion cannot be listed"
	assert len([ld async for ld in client2.discussion_locked_list() if ld.id == discussion2.id]) == 1, "locked discussion cannot be listed"

	# check discussion is not listed anymore
	assert len([ld async for ld in client1.discussion_list() if ld.id == discussion1.id]) == 0, "locked discussion still listed"
	assert len([ld async for ld in client2.discussion_list() if ld.id == discussion2.id]) == 0, "locked discussion still listed"

	# check discussion is not getable
	try:
		await client1.discussion_get(discussion_id=discussion1.id)
		assert False, "discussion still accessible"
	except grpc.aio.AioRpcError:
		pass
	try:
		await client2.discussion_get(discussion_id=discussion2.id)
		assert False, "discussion still accessible"
	except grpc.aio.AioRpcError:
		pass

	# actually we can do it, that's probably what we want to do
	# check we cannot list messages in a locked discussion
	# try:
	# 	messages = [m async for m in client1.message_list(datatypes.MessageFilter(discussion_id=discussion1.id))]
	# 	assert False, f"can list messages in a locked discussion: {messages}"
	# except grpc.aio.AioRpcError:
	# 	pass
	# try:
	# 	messages = [m async for m in client2.message_list(datatypes.MessageFilter(discussion_id=discussion2.id))]
	# 	assert False, f"can list messages in a locked discussion: {messages}"
	# except grpc.aio.AioRpcError:
	# 	pass

	# check we cannot send a message in a locked discussion
	try:
		await client1.message_send(discussion_id=discussion1.id, body="This message MUST NOT be sent")
		assert False, "can post in a locked discussion"
	except grpc.aio.AioRpcError:
		pass
	try:
		await client2.message_send(discussion_id=discussion2.id, body="This message MUST NOT be sent")
		assert False, "can post in a locked discussion"
	except grpc.aio.AioRpcError:
		pass

	# delete locked discussion
	await client1.discussion_locked_delete(discussion_id=discussion1.id)
	await client2.discussion_locked_delete(discussion_id=discussion2.id)

	# check discussion locked had been deleted
	assert len([ld async for ld in client1.discussion_locked_list() if ld.id == discussion1.id]) == 0, "deleted locked discussion can be listed"
	assert len([ld async for ld in client2.discussion_locked_list() if ld.id == discussion2.id]) == 0, "deleted locked discussion can be listed"

	# check discussion is not listed anymore
	assert len([ld async for ld in client1.discussion_list() if ld.id == discussion1.id]) == 0, "locked discussion still listed as normal after deletion"
	assert len([ld async for ld in client2.discussion_list() if ld.id == discussion2.id]) == 0, "locked discussion still listed as normal after deletion"

	# check discussion is not getable
	try:
		await client1.discussion_get(discussion_id=discussion1.id)
		assert False, "discussion still accessible"
	except grpc.aio.AioRpcError:
		pass
	try:
		await client2.discussion_get(discussion_id=discussion2.id)
		assert False, "discussion still accessible"
	except grpc.aio.AioRpcError:
		pass

	await upgrade_contact_to_one_to_one(client1, client2, contact1, contact2,
										ideal_discussion1=datatypes.Discussion(title=contact1.display_name),
										ideal_discussion2=datatypes.Discussion(title=contact2.display_name))

	new_contact_1: datatypes.Contact = await client1.contact_get(contact_id=contact1.id)
	# get new contact and check content
	new_contact_1._test_assertion(contact1)
	new_contact_2: datatypes.Contact = await client2.contact_get(contact_id=contact2.id)
	new_contact_2._test_assertion(contact2)


# noinspection PyProtectedMember
async def upgrade_contact_to_one_to_one(client1: ClientWrapper, client2: ClientWrapper, contact1: datatypes.Contact, contact2: datatypes.Contact, ideal_discussion1: datatypes.Discussion, ideal_discussion2: datatypes.Discussion):
	# prepare notification bots for one to one upgrade process
	contact1.has_one_to_one_discussion = True
	contact2.has_one_to_one_discussion = True

	# noinspection PyProtectedMember
	async def accept_invitation_handler(invitation: datatypes.Invitation):
		await invitation._client.invitation_accept(invitation.id)
	bots = [
		# client1: invitation sent, invitation deleted, contact new, discussion new
		client1.create_notification_bot(listeners.InvitationSentListener(handler=client1.get_check_content_handler(datatypes.Invitation(status=datatypes.Invitation.Status.STATUS_ONE_TO_ONE_INVITATION_WAIT_IT_TO_ACCEPT, display_name=contact1.display_name, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_SENT), count=1)),
		client1.create_notification_bot(listeners.InvitationDeletedListener(handler=client1.get_check_content_handler(datatypes.Invitation(status=datatypes.Invitation.Status.STATUS_ONE_TO_ONE_INVITATION_WAIT_IT_TO_ACCEPT, display_name=contact1.display_name, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_DELETED), count=1)),
		client1.create_notification_bot(listeners.ContactNewListener(handler=client1.get_check_content_handler(contact1, notification_type=listeners.NOTIFICATIONS.CONTACT_NEW), count=1)),
		client1.create_notification_bot(listeners.DiscussionNewListener(handler=client1.get_check_content_handler(ideal_discussion1, notification_type=listeners.NOTIFICATIONS.DISCUSSION_NEW), count=1)),

		# client2: invitation received (check content and accept it), invitation deleted, contact new, discussion new
		client2.create_notification_bot(listeners.InvitationReceivedListener(handler=client2.get_check_content_handler(datatypes.Invitation(status=datatypes.Invitation.Status.STATUS_ONE_TO_ONE_INVITATION_WAIT_YOU_TO_ACCEPT, display_name=contact2.display_name, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_SENT), count=1)),
		client2.create_notification_bot(listeners.InvitationReceivedListener(handler=accept_invitation_handler, count=1)),
		client2.create_notification_bot(listeners.InvitationDeletedListener(handler=client2.get_check_content_handler(datatypes.Invitation(status=datatypes.Invitation.Status.STATUS_ONE_TO_ONE_INVITATION_WAIT_YOU_TO_ACCEPT, display_name=contact2.display_name, sas=""), notification_type=listeners.NOTIFICATIONS.INVITATION_DELETED), count=1)),
		client2.create_notification_bot(listeners.ContactNewListener(handler=client2.get_check_content_handler(contact2, notification_type=listeners.NOTIFICATIONS.CONTACT_NEW), count=1)),
		client2.create_notification_bot(listeners.DiscussionNewListener(handler=client2.get_check_content_handler(ideal_discussion2, notification_type=listeners.NOTIFICATIONS.DISCUSSION_NEW), count=1)),
	]

	await client1.contact_invite_to_one_to_one_discussion(contact_id=contact1.id)

	for bot in bots:
		await bot.wait_for_listeners_end()
		await bot.stop()

	# wait for channel to be established
	await client1.wait_for_channel_creation()
	await client2.wait_for_channel_creation()
	logging.debug(f"channel created {client1.identity.id} <-> {client2.identity.id}")

	# get new contact and check content
	new_contact_1: datatypes.Contact = await client1.contact_get(contact_id=contact1.id)
	new_contact_1._test_assertion(contact1)
	new_contact_2: datatypes.Contact = await client2.contact_get(contact_id=contact2.id)
	new_contact_2._test_assertion(contact2)


async def test_update_details(client: ClientWrapper, client_holder: ClientHolder):
	# prepare new details for client2
	prev_details: datatypes.IdentityDetails = client.identity.details
	new_details: datatypes.IdentityDetails = datatypes.IdentityDetails(first_name=prev_details.first_name + "-UPDATED", last_name=prev_details.last_name + "-UPDATED", position=prev_details.position + "-UPDATED", company=prev_details.company + "-UPDATED")

	try:
		await update_details(client, client_holder, new_details)
		# update store identity in clientWrapper, we need up to date details to find associated contact / discussion in other clients
		client.identity = await client.identity_get()

		await update_details(client, client_holder, prev_details)
		# update store identity in clientWrapper, we need up to date details to find associated contact / discussion in other clients
		client.identity = await client.identity_get()

	# if something goes wrong try to restore previous details before exiting
	except Exception:
		await client.identity_update_details(prev_details)
		raise


# noinspection PyProtectedMember
async def update_details(client: ClientWrapper, client_holder: ClientHolder, new_details: datatypes.IdentityDetails):
	# prepare bot for notifications
	bots: list[OlvidClient] = []

	for other_client in [c for c in client_holder.clients if c != client]:
		contact: datatypes.Contact = await other_client.get_contact_associated_to_another_client(client)
		previous_details = contact.details
		contact.display_name = f"{new_details.first_name} {new_details.last_name} ({new_details.position} @ {new_details.company})"
		contact.details = new_details
		discussion: datatypes.Discussion = await other_client.get_discussion_associated_to_another_client(client)
		previous_title: str = discussion.title
		discussion.title = contact.display_name
		bots.extend([
			other_client.create_notification_bot(listeners.ContactDetailsUpdatedListener(handler=other_client.get_check_content_handler(contact._clone(), previous_details._clone(), notification_type=listeners.NOTIFICATIONS.CONTACT_DETAILS_UPDATED), count=1)),
			other_client.create_notification_bot(listeners.DiscussionTitleUpdatedListener(handler=other_client.get_check_content_handler(discussion._clone(), copy.deepcopy(previous_title), notification_type=listeners.NOTIFICATIONS.DISCUSSION_TITLE_UPDATED), count=1)),
		])

	await client.identity_update_details(new_details=new_details)

	for bot in bots:
		await bot.wait_for_listeners_end()
		await bot.stop()


async def test_get_identifier(c1: ClientWrapper):
	async for contact in c1.contact_list():
		identifier_1: bytes = await c1.contact_get_bytes_identifier(contact_id=contact.id)
		identifier_2: bytes = await c1.contact_get_bytes_identifier(contact_id=contact.id)
		assert identifier_1, "contact identifier is empty"
		assert identifier_1 == identifier_2, "contact identifier are not coherent"

async def test_invitation_link(c1: ClientWrapper):
	async for contact in c1.contact_list():
		link: str = await c1.contact_get_invitation_link(contact_id=contact.id)
		assert link, "empty contact invitation link"
		assert link.startswith("https://invitation.olvid.io/#"), f"Invalid contact invitation link format: {link}"
		assert len(link.removeprefix("https://invitation.olvid.io/#")) > 0, f"Invalid identity invitation link payload: {link}"

async def test_contact(client_holder: ClientHolder):
	for c1, c2 in client_holder.get_all_client_pairs():
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: prepare tests")
		await test_check_list_and_get_content(client_holder, c1, c2)
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: downgrade one to one")
		await test_down_upgrade_one_to_one_and_locked_discussions(c1, c2)
		logging.info(f"{c1.identity.id} <-> {c2.identity.id}: update contact details")
		await test_update_details(c1, client_holder)
		await test_get_identifier(c1)
		await test_invitation_link(c1)
